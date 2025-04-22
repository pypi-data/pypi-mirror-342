#  nuitka_build.py
#  Copyright (c) TotallyNotSeth 2025
#  All rights reserved.

# Compilation mode, standalone everywhere, except on macOS there app bundle
# nuitka-project: --mode=app
#
# Set EXE Filename
# nuitka-project: --output-filename=ttwhy
# nuitka-project: --output-dir=dist
#
# Add Package Data Files
# nuitka-project: --include-package-data=ttwhy:MxPlus_IBM_VGA_8x16.ttf
#
# Debugging options, controlled via environment variable at compile time.
# nuitka-project-if: {OS} == "Windows" and os.getenv("DEBUG_COMPILATION", "no") == "yes":
#     nuitka-project: --windows-console-mode=hide
# nuitka-project-else:
#     nuitka-project: --windows-console-mode=disable

if "__compiled__" in globals():  # If we are running in a nuitka executable
    from ttwhy.main import main
    from loguru import logger

    # noinspection PyBroadException
    try:
        main()  # Run the ttwhy demo
    except Exception:
        logger.exception("An unhandled exception occurred")
        raise
else:
    import os
    os.system("build.bat")  # Build and run the nuitka executable
