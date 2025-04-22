#  enforce_iverilog.py
#  Copyright (c) TotallyNotSeth 2025
#  All rights reserved.

# Builtin imports
import os
import shutil
from pathlib import Path

# Package imports
from loguru import logger


class InstallError(Exception):
    """Raised when an installation fails."""
    pass


def ensure_iverilog() -> None:
    """Ensures that iverilog is installed on the system, and installs it if it is not."""
    if shutil.which("iverilog"):
        logger.debug("Icarus Verilog is already installed")
        return

    logger.info("Icarus Verilog is not installed, prompting user for installation")
    os.system(str(Path(__file__).parent.parent / "iverilog-v12-20220611-x64_setup.exe"))

    if not shutil.which("iverilog"):
        raise InstallError("Icarus Verilog installation failed")

    logger.info("Icarus Verilog installation successful")


# Function test
if __name__ == "__main__":
    while True:
        try:
            ensure_iverilog()
            break
        except InstallError:
            continue
