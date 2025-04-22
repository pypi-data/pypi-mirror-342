import zipfile

import pytest

class DummyApp:
    """
    Dummy app for testing the hook.
    """
    def __init__(self, root, artifact_dir, project_name="test-project"):
        self.root = root
        self.artifact_dir = artifact_dir
        self.project_name = project_name
        
    def display_mini_status(self, plugin, msg):
        """
        Mock implementation of display_mini_status.
        """
        pass

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
    
    calls = []
    monkeypatch.setattr('subprocess.check_call', lambda cmd, cwd: calls.append((cmd, cwd)))
    
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
        'calls': calls,
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
    
    calls = []
    monkeypatch.setattr('subprocess.check_call', lambda cmd, cwd: calls.append((cmd, cwd)))
    
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
        'calls': calls,
    }