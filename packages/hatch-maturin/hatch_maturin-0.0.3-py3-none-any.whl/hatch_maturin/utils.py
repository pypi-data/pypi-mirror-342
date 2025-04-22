from __future__ import annotations

import sysconfig
from typing import Optional
import subprocess
import shutil

def get_python_path(target_python: Optional[str] = None) -> str:
    if target_python:
        return target_python
    
    return sysconfig.get_paths()["scripts"].replace("bin", "python")

def is_rust_installed() -> bool:
    import subprocess
    import shutil
    
    rustc_path = shutil.which("rustc")
    if rustc_path is not None:
        return True
    
    try:
        subprocess.run(
            ["rustc", "--version"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False
    
def check_maturin_installed() -> bool:
    
    maturin_path = shutil.which("maturin")
    if maturin_path is not None:
        return True
    
    try:
        subprocess.run(
            ["maturin", "--version"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False