import os
from pathlib import Path
def get_keypath(key_name):
    working_dir = Path(os.curdir)
    key_path = working_dir / "keys" / f"key_{key_name}.txt"
    return key_path