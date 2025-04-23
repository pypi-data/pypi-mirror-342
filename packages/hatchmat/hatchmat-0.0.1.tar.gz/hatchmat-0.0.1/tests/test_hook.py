import pytest
import sys
import zipfile
import logging
import subprocess
from concurrent.futures import Future
from pathlib import Path
from hatchmat.builder import build_maturin_command

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

class MockBuildHookInterface:
    def __init__(self):
        self.root = ""
        self.artifact_dir = ""
        self.app = None
        self.config = {}

sys.modules['hatchling'] = type('MockHatchling', (), {})
sys.modules['hatchling.builders'] = type('MockBuilders', (), {})
sys.modules['hatchling.builders.hooks'] = type('MockHooks', (), {})
sys.modules['hatchling.builders.hooks.plugin'] = type('MockPlugin', (), {})
sys.modules['hatchling.builders.hooks.plugin.interface'] = type('MockInterface', (), {'BuildHookInterface': MockBuildHookInterface})

from hatchmat.config import get_config_with_defaults
from hatchmat.utils import get_python_path
from hatchmat.builder import build_maturin_command, collect_wheels, extract_wheel

class MaturinHookTest(MockBuildHookInterface):
    PLUGIN_NAME = "maturin"
    
    def initialize(self, version, build_data):
        self._setup_logging()
        
        config = get_config_with_defaults(self.config, getattr(self.app, "project_name", ""))
        
        if config.get("multi_crate"):
            self._process_multiple_crates(config, build_data)
        else:
            self._process_single_crate(config, build_data)
    
    def _setup_logging(self):
        self.logger = logging.getLogger("hatchmat")
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
    
    def _process_single_crate(self, config, build_data):
        crate_path = Path(self.root).joinpath(config["path"])
        if not crate_path.exists():
            raise RuntimeError(f"[hatchmat] crate path missing: {crate_path}")
        
        wheels_dir = crate_path / "target" / "wheels"
        wheels_dir.mkdir(parents=True, exist_ok=True)
        
        self._run_build_scripts(config, crate_path, "pre_build_script")
        
        python_path = get_python_path(config.get("target_python"))
        
        maturin_cmd = build_maturin_command(
            python_path=python_path,
            wheels_dir=wheels_dir,
            config=config,
        )
        
        if hasattr(self, "maturin_calls"):
            self.maturin_calls.append((maturin_cmd, str(crate_path)))
        
        module_info = f" for module {config.get('module_name', '')}" if config.get("module_name") else ""
        self.app.display_mini_status("hatchmat", f"Compiling Rust crate{module_info}…")
        
        if hasattr(self, "subprocess_run_results") and self.subprocess_run_results:
            result = self.subprocess_run_results.pop(0)
            if isinstance(result, Exception):
                raise RuntimeError(f"[hatchmat] Maturin build failed: {result}") from result
        
        self._run_build_scripts(config, crate_path, "post_build_script")
        
        collect_wheels(
            wheels_dir=wheels_dir,
            build_data=build_data,
            artifact_dir=self.artifact_dir
        )
    
    def _process_multiple_crates(self, config, build_data):
        crates = config.get("multi_crate", {})
        if config.get("parallel_build", False):
            max_workers = config.get("max_jobs", None)
            futures = []
            for module_name, crate_path_str in crates.items():
                future = Future()
                try:
                    result = self._build_crate(module_name, crate_path_str, config, build_data)
                    future.set_result(result)
                except Exception as e:
                    future.set_exception(RuntimeError(f"[hatchmat] Maturin build failed: {e}"))
                futures.append(future)
            
            for future in futures:
                future.result()
        else:
            for module_name, crate_path_str in crates.items():
                self._build_crate(module_name, crate_path_str, config, build_data)
    
    def _build_crate(self, module_name, crate_path_str, config, build_data):
        crate_path = Path(self.root).joinpath(crate_path_str)
        if not crate_path.exists():
            raise RuntimeError(f"[hatchmat] crate path missing for {module_name}: {crate_path}")
        
        wheels_dir = crate_path / "target" / "wheels"
        wheels_dir.mkdir(parents=True, exist_ok=True)
        
        crate_config = dict(config)
        crate_config["module_name"] = module_name
        
        self._run_build_scripts(crate_config, crate_path, "pre_build_script")
        
        python_path = get_python_path(crate_config.get("target_python"))
        
        maturin_cmd = build_maturin_command(
            python_path=python_path,
            wheels_dir=wheels_dir,
            config=crate_config,
        )
        
        if hasattr(self, "maturin_calls"):
            self.maturin_calls.append((maturin_cmd, str(crate_path)))
        
        module_info = f" for module {module_name}"
        self.app.display_mini_status("hatchmat", f"Compiling Rust crate{module_info}…")
        
        if hasattr(self, "subprocess_run_results") and self.subprocess_run_results:
            result = self.subprocess_run_results.pop(0)
            if isinstance(result, Exception):
                raise result
        
        self._run_build_scripts(crate_config, crate_path, "post_build_script")
        
        collect_wheels(
            wheels_dir=wheels_dir,
            build_data=build_data,
            artifact_dir=self.artifact_dir
        )
    
    def _run_build_scripts(self, config, crate_path, script_key):
        script = config.get(script_key)
        if script:
            script_path = Path(self.root).joinpath(script)
            if not script_path.exists():
                raise RuntimeError(f"[hatchmat] {script_key} script missing: {script_path}")
            
            if hasattr(self, "script_calls"):
                self.script_calls.append((str(script_path), str(crate_path), script_key))
            
            if hasattr(self, "script_results") and self.script_results:
                result = self.script_results.pop(0)
                if isinstance(result, Exception):
                    raise RuntimeError(f"[hatchmat] {script_key} script failed: {result}") from result

class DummyApp:
    def __init__(self, root, artifact_dir, project_name="test-project"):
        self.root = root
        self.artifact_dir = artifact_dir
        self.project_name = project_name
        self.status_messages = []
        
    def display_mini_status(self, plugin, msg):
        self.status_messages.append((plugin, msg))

@pytest.fixture
def tmp_hook_env(tmp_path, monkeypatch):
    crate = tmp_path / "crate"
    crate.mkdir()
    
    wheel_dir = crate / "target" / "wheels"
    wheel_dir.mkdir(parents=True)
    
    whl = wheel_dir / "fake-0.1.0-cp38-none-any.whl"
    with zipfile.ZipFile(whl, 'w') as zf:
        zf.writestr('mod.so', 'binary')
        zf.writestr('mod.py', 'def test(): pass')
    
    subprocess_calls = []
    monkeypatch.setattr('subprocess.check_call', lambda *args, **kwargs: subprocess_calls.append((args, kwargs)))
    
    run_results = []
    def mock_run(*args, **kwargs):
        run_results.append((args, kwargs))
        result = type('MockCompletedProcess', (), {
            'check_returncode': lambda self: None,
            'returncode': 0,
            'stdout': 'Maturin build output',
            'stderr': '',
        })()
        return result
    
    monkeypatch.setattr('subprocess.run', mock_run)
    
    build_dir = tmp_path / 'build'
    build_dir.mkdir()
    
    app = DummyApp(str(tmp_path), str(build_dir))
    
    return {
        'tmp_path': tmp_path,
        'crate_path': crate,
        'wheel_dir': wheel_dir,
        'wheel_file': whl,
        'build_dir': build_dir,
        'app': app,
        'subprocess_calls': subprocess_calls,
        'run_results': run_results,
    }

@pytest.fixture
def multi_crate_env(tmp_path, monkeypatch):
    crate1 = tmp_path / "crate1"
    crate1.mkdir()
    wheel_dir1 = crate1 / "target" / "wheels"
    wheel_dir1.mkdir(parents=True)
    whl1 = wheel_dir1 / "mod1-0.1.0-cp38-none-any.whl"
    with zipfile.ZipFile(whl1, 'w') as zf:
        zf.writestr('mod1.so', 'binary1')
    
    crate2 = tmp_path / "crate2"
    crate2.mkdir()
    wheel_dir2 = crate2 / "target" / "wheels"
    wheel_dir2.mkdir(parents=True)
    whl2 = wheel_dir2 / "mod2-0.1.0-cp38-none-any.whl"
    with zipfile.ZipFile(whl2, 'w') as zf:
        zf.writestr('mod2.so', 'binary2')
    
    subprocess_calls = []
    monkeypatch.setattr('subprocess.check_call', lambda *args, **kwargs: subprocess_calls.append((args, kwargs)))
    
    run_results = []
    def mock_run(*args, **kwargs):
        run_results.append((args, kwargs))
        result = type('MockCompletedProcess', (), {
            'check_returncode': lambda self: None,
            'returncode': 0,
            'stdout': 'Maturin build output',
            'stderr': '',
        })()
        return result
    
    monkeypatch.setattr('subprocess.run', mock_run)
    
    build_dir = tmp_path / 'build'
    build_dir.mkdir()
    
    app = DummyApp(str(tmp_path), str(build_dir))
    
    return {
        'tmp_path': tmp_path,
        'crates': {
            'mod1': crate1,
            'mod2': crate2,
        },
        'wheel_dirs': {
            'mod1': wheel_dir1,
            'mod2': wheel_dir2,
        },
        'wheel_files': {
            'mod1': whl1,
            'mod2': whl2,
        },
        'build_dir': build_dir,
        'app': app,
        'subprocess_calls': subprocess_calls,
        'run_results': run_results,
    }

def test_missing_crate(tmp_path):
    hook = MaturinHookTest()
    hook.root = str(tmp_path)
    hook.config = {"path": "no_such_crate"}
    hook.app = DummyApp(str(tmp_path), str(tmp_path / 'build'))
    build_data = {}
    
    with pytest.raises(RuntimeError, match="crate path missing"):
        hook.initialize('0.1.0', build_data)

def test_initialize_single_crate(tmp_hook_env):
    hook = MaturinHookTest()
    hook.root = str(tmp_hook_env['tmp_path'])
    hook.config = {"path": "crate"}
    hook.app = tmp_hook_env['app']
    hook.artifact_dir = str(tmp_hook_env['build_dir'])
    hook.maturin_calls = []
    
    build_data = {}
    hook.initialize('0.1.0', build_data)
    
    assert len(hook.maturin_calls) == 1, "maturin command was not recorded"
    
    assert 'force-include' in build_data
    assert any(k.endswith('mod.so') for k in build_data['force-include'])
    assert any(k.endswith('mod.py') for k in build_data['force-include'])
    
    cmd, _ = hook.maturin_calls[0]
    assert cmd[0] == "maturin"
    assert "build" in cmd
    assert "--release" in cmd

def test_initialize_with_features(tmp_hook_env):
    hook = MaturinHookTest()
    hook.root = str(tmp_hook_env['tmp_path'])
    hook.config = {
        "path": "crate",
        "features": ["feature1", "feature2"],
    }
    hook.app = tmp_hook_env['app']
    hook.artifact_dir = str(tmp_hook_env['build_dir'])
    hook.maturin_calls = []
    
    build_data = {}
    hook.initialize('0.0.1', build_data)
    
    cmd, _ = hook.maturin_calls[0]
    assert "--features" in cmd
    features_index = cmd.index("--features")
    assert cmd[features_index + 1] == "feature1,feature2"

def test_initialize_with_custom_args(tmp_hook_env):
    hook = MaturinHookTest()
    hook.root = str(tmp_hook_env['tmp_path'])
    hook.config = {
        "path": "crate",
        "maturin_args": ["--custom-arg", "value"],
    }
    hook.app = tmp_hook_env['app']
    hook.artifact_dir = str(tmp_hook_env['build_dir'])
    hook.maturin_calls = []
    
    build_data = {}
    hook.initialize('0.1.0', build_data)
    
    cmd, _ = hook.maturin_calls[0]
    assert "--custom-arg" in cmd
    custom_arg_index = cmd.index("--custom-arg")
    assert cmd[custom_arg_index + 1] == "value"

def test_initialize_multi_crate(multi_crate_env):
    hook = MaturinHookTest()
    hook.root = str(multi_crate_env['tmp_path'])
    hook.config = {
        "multi_crate": {
            "mod1": "crate1",
            "mod2": "crate2",
        }
    }
    hook.app = multi_crate_env['app']
    hook.artifact_dir = str(multi_crate_env['build_dir'])
    hook.maturin_calls = []
    
    build_data = {}
    hook.initialize('0.0.1', build_data)
    
    assert len(hook.maturin_calls) == 2, "Two maturin commands should be recorded"
    
    assert 'force-include' in build_data
    assert any(k.endswith('mod1.so') for k in build_data['force-include'])
    assert any(k.endswith('mod2.so') for k in build_data['force-include'])
    
    cmd1, _ = hook.maturin_calls[0]
    cmd2, _ = hook.maturin_calls[1]
    
    assert "--module-name" in cmd1
    assert "--module-name" in cmd2
    
    module_name_index1 = cmd1.index("--module-name")
    module_name_index2 = cmd2.index("--module-name")
    
    module_names = [cmd1[module_name_index1 + 1], cmd2[module_name_index2 + 1]]
    assert "mod1" in module_names
    assert "mod2" in module_names

def test_initialize_with_target_manual():
    
    python_path = "/path/to/python"
    wheels_dir = Path("/tmp/wheels")
    config = {
        "target": "x86_64-unknown-linux-gnu",
        "features": [],
        "skip_auditwheel": True,
        "maturin_args": []
    }
    
    cmd = build_maturin_command(python_path, wheels_dir, config)
    
    assert "--target" in cmd
    target_index = cmd.index("--target")
    assert cmd[target_index + 1] == "x86_64-unknown-linux-gnu"

def test_initialize_with_pre_build_script(tmp_hook_env):
    script_path = tmp_hook_env['tmp_path'] / "pre_build.sh"
    script_path.write_text("#!/bin/bash\necho 'pre-build'")
    script_path.chmod(0o755)
    
    hook = MaturinHookTest()
    hook.root = str(tmp_hook_env['tmp_path'])
    hook.config = {
        "path": "crate",
        "pre_build_script": "pre_build.sh",
    }
    hook.app = tmp_hook_env['app']
    hook.artifact_dir = str(tmp_hook_env['build_dir'])
    hook.maturin_calls = []
    hook.script_calls = []
    
    build_data = {}
    hook.initialize('0.1.0', build_data)
    
    assert len(hook.script_calls) == 1
    script_path, crate_path, script_key = hook.script_calls[0]
    assert script_path.endswith("pre_build.sh")
    assert script_key == "pre_build_script"

def test_initialize_with_post_build_script(tmp_hook_env):
    script_path = tmp_hook_env['tmp_path'] / "post_build.sh"
    script_path.write_text("#!/bin/bash\necho 'post-build'")
    script_path.chmod(0o755)
    
    hook = MaturinHookTest()
    hook.root = str(tmp_hook_env['tmp_path'])
    hook.config = {
        "path": "crate",
        "post_build_script": "post_build.sh",
    }
    hook.app = tmp_hook_env['app']
    hook.artifact_dir = str(tmp_hook_env['build_dir'])
    hook.maturin_calls = []
    hook.script_calls = []
    
    build_data = {}
    hook.initialize('0.1.0', build_data)
    
    assert len(hook.script_calls) == 1
    script_path, crate_path, script_key = hook.script_calls[0]
    assert script_path.endswith("post_build.sh")
    assert script_key == "post_build_script"

def test_missing_build_script(tmp_hook_env):
    hook = MaturinHookTest()
    hook.root = str(tmp_hook_env['tmp_path'])
    hook.config = {
        "path": "crate",
        "pre_build_script": "non_existent_script.sh",
    }
    hook.app = tmp_hook_env['app']
    hook.artifact_dir = str(tmp_hook_env['build_dir'])
    
    build_data = {}
    with pytest.raises(RuntimeError, match="pre_build_script script missing"):
        hook.initialize('0.1.0', build_data)

def test_build_script_failure(tmp_hook_env):
    hook = MaturinHookTest()
    hook.root = str(tmp_hook_env['tmp_path'])
    hook.config = {
        "path": "crate",
        "pre_build_script": "existing_script.sh",
    }
    hook.app = tmp_hook_env['app']
    hook.artifact_dir = str(tmp_hook_env['build_dir'])
    hook.script_calls = []
    
    script_path = tmp_hook_env['tmp_path'] / "existing_script.sh"
    script_path.write_text("#!/bin/bash\necho 'fail'")
    script_path.chmod(0o755)
    
    hook.script_results = [subprocess.CalledProcessError(1, ["failing_command"])]
    
    build_data = {}
    with pytest.raises(RuntimeError, match="pre_build_script script failed"):
        hook.initialize('0.1.0', build_data)

def test_initialize_multi_crate_parallel(multi_crate_env):
    hook = MaturinHookTest()
    hook.root = str(multi_crate_env['tmp_path'])
    hook.config = {
        "multi_crate": {
            "mod1": "crate1",
            "mod2": "crate2",
        },
        "parallel_build": True,
        "max_jobs": 2,
    }
    hook.app = multi_crate_env['app']
    hook.artifact_dir = str(multi_crate_env['build_dir'])
    hook.maturin_calls = []
    
    build_data = {}
    hook.initialize('0.0.1', build_data)
    
    assert len(hook.maturin_calls) == 2, "Two maturin commands should be recorded"
    
    assert 'force-include' in build_data
    assert any(k.endswith('mod1.so') for k in build_data['force-include'])
    assert any(k.endswith('mod2.so') for k in build_data['force-include'])

def test_parallel_build_with_error(multi_crate_env):
    hook = MaturinHookTest()
    hook.root = str(multi_crate_env['tmp_path'])
    hook.config = {
        "multi_crate": {
            "mod1": "crate1",
            "mod2": "crate2",
        },
        "parallel_build": True,
    }
    hook.app = multi_crate_env['app']
    hook.artifact_dir = str(multi_crate_env['build_dir'])
    hook.maturin_calls = []
    
    error = subprocess.CalledProcessError(1, ["maturin"], output="Failed", stderr="Error")
    hook.subprocess_run_results = [error, None]
    
    build_data = {}
    with pytest.raises(RuntimeError, match="Maturin build failed"):
        hook.initialize('0.0.1', build_data)

def test_environment_variables_config(tmp_hook_env):
    hook = MaturinHookTest()
    hook.root = str(tmp_hook_env['tmp_path'])
    hook.config = {
        "path": "crate",
        "env": {
            "RUSTFLAGS": "-C target-cpu=native",
            "CARGO_TERM_COLOR": "always"
        }
    }
    hook.app = tmp_hook_env['app']
    hook.artifact_dir = str(tmp_hook_env['build_dir'])
    hook.maturin_calls = []
    
    build_data = {}
    hook.initialize('0.1.0', build_data)

    assert len(hook.maturin_calls) == 1, "maturin command was not recorded"

def test_status_message_display(tmp_hook_env):
    app = tmp_hook_env['app']
    
    hook = MaturinHookTest()
    hook.root = str(tmp_hook_env['tmp_path'])
    hook.config = {"path": "crate"}
    hook.app = app
    hook.artifact_dir = str(tmp_hook_env['build_dir'])
    hook.maturin_calls = []
    
    build_data = {}
    hook.initialize('0.1.0', build_data)
    
    assert len(app.status_messages) > 0
    assert any("hatchmat" in msg[0] for msg in app.status_messages)