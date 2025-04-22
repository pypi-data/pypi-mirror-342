from __future__ import annotations

from typing import Dict, Any

def get_config_with_defaults(config: Dict[str, Any], package_name: str = "") -> Dict[str, Any]:
    result = dict(config)
    
    default_crate_path = package_name.replace("-", "_") if package_name else "src"
    
    result.setdefault("path", default_crate_path)
    result.setdefault("features", [])
    result.setdefault("maturin_args", [])
    result.setdefault("skip_auditwheel", True)
    result.setdefault("target_python", None)
    
    return result

def get_platform_specific_config(config: Dict[str, Any]) -> Dict[str, Any]:
    import platform
    
    result = dict(config)
    system = platform.system().lower()
    
    platform_config = config.get(f"platform_{system}", {})
    if platform_config:
        for key, value in platform_config.items():
            result[key] = value
    
    return result