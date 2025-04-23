import os
import zipfile

from pathlib import Path
from hatchmat.builder import build_maturin_command, collect_wheels

def test_build_maturin_command_basic():
    python_path = "/path/to/python"
    wheels_dir = Path("/path/to/wheels")
    config = {
        "features": [],
        "maturin_args": [],
        "skip_auditwheel": True,
    }
    
    cmd = build_maturin_command(python_path, wheels_dir, config)
    
    assert cmd[0] == "maturin"
    assert "build" in cmd
    assert "--release" in cmd
    assert "--interpreter" in cmd
    assert python_path in cmd
    assert "--out" in cmd
    assert str(wheels_dir) in cmd
    assert "--skip-auditwheel" in cmd

def test_build_maturin_command_features():
    python_path = "/path/to/python"
    wheels_dir = Path("/path/to/wheels")
    config = {
        "features": ["feature1", "feature2"],
        "maturin_args": [],
        "skip_auditwheel": True,
    }
    
    cmd = build_maturin_command(python_path, wheels_dir, config)
    
    assert "--features" in cmd
    features_index = cmd.index("--features")
    assert cmd[features_index + 1] == "feature1,feature2"

def test_build_maturin_command_module_name():
    python_path = "/path/to/python"
    wheels_dir = Path("/path/to/wheels")
    config = {
        "features": [],
        "maturin_args": [],
        "skip_auditwheel": True,
        "module_name": "custom_module",
    }
    
    cmd = build_maturin_command(python_path, wheels_dir, config)
    
    assert "--module-name" in cmd
    module_name_index = cmd.index("--module-name")
    assert cmd[module_name_index + 1] == "custom_module"

def test_build_maturin_command_custom_args():
    python_path = "/path/to/python"
    wheels_dir = Path("/path/to/wheels")
    config = {
        "features": [],
        "maturin_args": ["--custom-arg", "value", "--flag"],
        "skip_auditwheel": True,
    }
    
    cmd = build_maturin_command(python_path, wheels_dir, config)
    
    assert "--custom-arg" in cmd
    assert "value" in cmd
    assert "--flag" in cmd

def test_collect_wheels_empty(tmp_path):
    wheels_dir = tmp_path / "wheels"
    wheels_dir.mkdir()
    build_data = {}
    artifact_dir = str(tmp_path / "artifacts")
    
    collect_wheels(wheels_dir, build_data, artifact_dir)
    
    assert "force-include" in build_data
    assert len(build_data["force-include"]) == 0

def test_collect_wheels(tmp_path):
    
    wheels_dir = tmp_path / "wheels"
    wheels_dir.mkdir()
    
    wheel1_path = wheels_dir / "module1-0.1.0-cp38-none-any.whl"
    with zipfile.ZipFile(wheel1_path, 'w') as zf:
        zf.writestr('module1.so', 'binary content')
        zf.writestr('module1.py', 'python content')
        zf.writestr('module1.pyi', 'type hints')
        zf.writestr('not_extracted.txt', 'text content')
    
    wheel2_path = wheels_dir / "module2-0.1.0-cp38-none-any.whl"
    with zipfile.ZipFile(wheel2_path, 'w') as zf:
        zf.writestr('module2.so', 'binary content')
        zf.writestr('subpkg/module2_sub.py', 'python content')
    
    artifact_dir = tmp_path / "artifacts"
    artifact_dir.mkdir()
    
    build_data = {}
    collect_wheels(wheels_dir, build_data, str(artifact_dir))
    
    assert "force-include" in build_data
    force_include = build_data["force-include"]
    
    expected_files = [
        'module1.so',
        'module1.py',
        'module1.pyi',
        'module2.so',
        os.path.join('subpkg', 'module2_sub.py'),
    ]
    
    for expected_file in expected_files:
        assert any(expected_file in k for k in force_include.keys())
    
    assert not any('not_extracted.txt' in k for k in force_include.keys())