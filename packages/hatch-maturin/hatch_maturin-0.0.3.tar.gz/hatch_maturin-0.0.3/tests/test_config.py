from hatch_maturin.config import get_config_with_defaults, get_platform_specific_config

def test_get_config_with_defaults_empty():

    config = get_config_with_defaults({})
    
    assert "path" in config
    assert "features" in config
    assert "maturin_args" in config
    assert "skip_auditwheel" in config
    assert "target_python" in config
    
    assert isinstance(config["features"], list)
    assert isinstance(config["maturin_args"], list)
    assert config["skip_auditwheel"] is True
    assert config["target_python"] is None

def test_get_config_with_defaults_package_name():
    config = get_config_with_defaults({}, "test-package")
    
    assert config["path"] == "test_package"

def test_get_config_with_defaults_override():
    user_config = {
        "path": "custom_path",
        "features": ["custom_feature"],
        "skip_auditwheel": False,
    }
    
    config = get_config_with_defaults(user_config)
    
    assert config["path"] == "custom_path"
    assert config["features"] == ["custom_feature"]
    assert config["skip_auditwheel"] is False
    assert "maturin_args" in config
    assert "target_python" in config

def test_get_platform_specific_config(monkeypatch):
    monkeypatch.setattr('platform.system', lambda: "Linux")
    
    base_config = {
        "path": "base_path",
        "features": ["base_feature"],
        "platform_linux": {
            "path": "linux_path",
            "maturin_args": ["--linux-arg"],
        },
        "platform_windows": {
            "path": "windows_path",
        },
    }
    
    config = get_platform_specific_config(base_config)
    
    assert config["path"] == "linux_path"
    assert config["features"] == ["base_feature"]
    assert config["maturin_args"] == ["--linux-arg"]
    
    assert "platform_linux" in config
    assert "platform_windows" in config

def test_get_platform_specific_config_no_platform_match(monkeypatch):
    monkeypatch.setattr('platform.system', lambda: "Darwin")
    
    base_config = {
        "path": "base_path",
        "features": ["base_feature"],
        "platform_linux": {
            "path": "linux_path",
        },
        "platform_windows": {
            "path": "windows_path",
        },
    }
    
    config = get_platform_specific_config(base_config)
    
    assert config["path"] == "base_path"
    assert config["features"] == ["base_feature"]

    assert "platform_linux" in config
    assert "platform_windows" in config