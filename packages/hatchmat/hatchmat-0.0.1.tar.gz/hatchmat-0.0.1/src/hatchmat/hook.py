from __future__ import annotations

import logging
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Dict, Any

from hatchling.builders.hooks.plugin.interface import BuildHookInterface

from hatchmat.config import get_config_with_defaults
from hatchmat.builder import build_crate, collect_wheels

logger = logging.getLogger(__name__)

class MaturinHook(BuildHookInterface):
    PLUGIN_NAME = "maturin"

    def initialize(self, version: str, build_data: dict) -> None:
        self._setup_logging()
        
        config = get_config_with_defaults(self.config, getattr(self.app, "project_name", ""))
        
        if config.get("multi_crate"):
            self._process_multiple_crates(config, build_data)
        else:
            self._process_single_crate(config, build_data)
            
        logger.info("Maturin build completed successfully")

    def _setup_logging(self) -> None:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

    def _process_single_crate(self, config: Dict[str, Any], build_data: Dict[str, Any]) -> None:
        crate_path = Path(self.root).joinpath(config["path"])
        if not crate_path.exists():
            raise RuntimeError(f"[hatchmat] crate path missing: {crate_path}")
        
        wheels_dir = crate_path / "target" / "wheels"
        wheels_dir.mkdir(parents=True, exist_ok=True)
        
        self._run_build_scripts(config, crate_path, "pre_build_script")
        build_crate(
            crate_path=crate_path,
            config=config,
            wheels_dir=wheels_dir,
            app=self.app
        )
        self._run_build_scripts(config, crate_path, "post_build_script")
        
        collect_wheels(
            wheels_dir=wheels_dir,
            build_data=build_data,
            artifact_dir=self.artifact_dir
        )

    def _process_multiple_crates(self, config: Dict[str, Any], build_data: Dict[str, Any]) -> None:
        crates = config.get("multi_crate", {})
        if config.get("parallel_build", False):
            max_workers = config.get("max_jobs", None)
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = []
                for module_name, crate_path_str in crates.items():
                    futures.append(executor.submit(self._build_crate, module_name, crate_path_str, config, build_data))
                for future in futures:
                    future.result()
        else:
            for module_name, crate_path_str in crates.items():
                self._build_crate(module_name, crate_path_str, config, build_data)

    def _build_crate(self, module_name: str, crate_path_str: str, config: Dict[str, Any], build_data: Dict[str, Any]) -> None:
        crate_path = Path(self.root).joinpath(crate_path_str)
        if not crate_path.exists():
            raise RuntimeError(f"[hatchmat] crate path missing for {module_name}: {crate_path}")
        
        wheels_dir = crate_path / "target" / "wheels"
        wheels_dir.mkdir(parents=True, exist_ok=True)
        
        crate_config = dict(config)
        crate_config["module_name"] = module_name
        
        self._run_build_scripts(crate_config, crate_path, "pre_build_script")
        build_crate(
            crate_path=crate_path,
            config=crate_config,
            wheels_dir=wheels_dir,
            app=self.app
        )
        self._run_build_scripts(crate_config, crate_path, "post_build_script")
        
        collect_wheels(
            wheels_dir=wheels_dir,
            build_data=build_data,
            artifact_dir=self.artifact_dir
        )

    def _run_build_scripts(self, config: Dict[str, Any], crate_path: Path, script_key: str) -> None:
        script = config.get(script_key)
        if script:
            script_path = Path(self.root).joinpath(script)
            if not script_path.exists():
                raise RuntimeError(f"[hatchmat] {script_key} script missing: {script_path}")
            try:
                subprocess.check_call([str(script_path)], cwd=crate_path)
            except subprocess.CalledProcessError as e:
                raise RuntimeError(f"[hatchmat] {script_key} script failed: {e}") from e