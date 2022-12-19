import os
from pathlib import Path


def get_keypath(key_name):
    working_dir = Path(__file__).parent.resolve()
    key_path = working_dir / "keys" / f"key_{key_name}.txt"
    return key_path
