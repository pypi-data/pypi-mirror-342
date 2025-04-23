from __future__ import annotations

import logging
import os
import shutil
import subprocess
import zipfile
from pathlib import Path
from typing import Dict, Any, List

from .utils import get_python_path

logger = logging.getLogger(__name__)

def build_crate(
    crate_path: Path,
    config: Dict[str, Any],
    wheels_dir: Path,
    app: Any,
) -> None:
    """
    Args:
        crate_path: Path to the Rust crate
        config: Configuration dictionary
        wheels_dir: Directory where wheels will be saved
        app: Hatch application instance
    """
    python_path = get_python_path(config.get("target_python"))
    
    maturin_cmd = build_maturin_command(
        python_path=python_path,
        wheels_dir=wheels_dir,
        config=config,
    )
    
    module_info = f" for module {config['module_name']}" if "module_name" in config else ""
    app.display_mini_status("hatchmat", f"Compiling Rust crate{module_info}…")
    logger.info(f"Running: {' '.join(maturin_cmd)}")
    
    try:
        subprocess.check_call(maturin_cmd, cwd=crate_path)
    except subprocess.CalledProcessError as e:
        logger.error(f"Maturin build failed with exit code {e.returncode}")
        raise RuntimeError(f"[hatchmat] Maturin build failed: {e}") from e

def build_maturin_command(
    python_path: str,
    wheels_dir: Path,
    config: Dict[str, Any],
) -> List[str]:
    """
    Args:
        python_path: Path to the Python interpreter
        wheels_dir: Directory where wheels will be saved
        config: Configuration dictionary
    """
    cmd = [
        "maturin",
        "build",
        "--release",
        "--interpreter",
        python_path,
        "--out",
        str(wheels_dir),
    ]
    
    if "module_name" in config:
        cmd.extend(["--module-name", config["module_name"]])
    
    if config["features"]:
        features_str = ",".join(config["features"])
        cmd.extend(["--features", features_str])
    
    if config["skip_auditwheel"]:
        cmd.append("--skip-auditwheel")
    
    if "target" in config:
        cmd.extend(["--target", config["target"]])
    
    cmd.extend(config.get("maturin_args", []))

    return cmd

def collect_wheels(
    wheels_dir: Path,
    build_data: Dict[str, Any],
    artifact_dir: str,
) -> None:
    build_data.setdefault("force-include", {})
    wheel_count = 0
    
    for wheel in wheels_dir.glob("*.whl"):
        wheel_count += 1
        extract_wheel(
            wheel=wheel,
            build_data=build_data,
            artifact_dir=artifact_dir,
        )
    
    if wheel_count == 0:
        logger.warning("No wheels were found after Maturin build")

def extract_wheel(wheel: Path, build_data: Dict[str, Any], artifact_dir: str) -> None:
    logger.info(f"Extracting wheel: {wheel.name}")
    dest = Path(artifact_dir)
    
    with zipfile.ZipFile(wheel) as zf:
        for member in zf.namelist():
            member_path = Path(member)
            if member_path.is_absolute() or '..' in member_path.parts:
                logger.warning(f"Skipping path in wheel: {member}")
                continue
                
            if member.endswith((".so", ".pyd", ".py", ".pyi")):
                target = dest / member
                target.parent.mkdir(parents=True, exist_ok=True)
                
                with zf.open(member) as src, open(target, "wb") as dst:
                    shutil.copyfileobj(src, dst)
                
                rel = os.path.relpath(target, dest)
                build_data["force-include"][rel] = rel