#!/usr/bin/env python3

import subprocess
from pathlib import Path
from utils import setup_logging

logger = setup_logging('update_all')
script_dir = Path(__file__).parent

failed_scripts = []
successful_scripts = []

for script in sorted(script_dir.glob("update_*.py")):
    if script.name != "update_all.py":
        logger.info(f"running {script.name}...")
        result = subprocess.run(["python3", str(script)])

        if result.returncode == 0:
            successful_scripts.append(script.name)
        else:
            failed_scripts.append(script.name)
            logger.error(f"failed: {script.name}")

logger.info(f"success: {len(successful_scripts)}, failed: {len(failed_scripts)}")
if failed_scripts:
    logger.error(f"failed scripts: {', '.join(failed_scripts)}")
    exit(1)
