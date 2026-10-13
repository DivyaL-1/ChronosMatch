import os
import sys
import tempfile


def pickle_endpoint(name: str = "market_firehose_proof") -> str:
    if sys.platform == "win32":
        return f"\\\\.\\pipe\\{name}"
    return os.path.join(tempfile.gettempdir(), f"{name}.sock")


def scratch_path(filename: str) -> str:
    return os.path.join(tempfile.gettempdir(), filename)


def is_removable_file(address: str) -> bool:
    return not address.startswith("\\\\")
