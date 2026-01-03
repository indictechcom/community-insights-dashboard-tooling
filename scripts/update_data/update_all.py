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
        try:
            result = subprocess.run(
                ["python3", str(script)],
                timeout=3600
            )

            if result.returncode == 0:
                successful_scripts.append(script.name)
                logger.info(f"completed: {script.name}")
            else:
                failed_scripts.append(script.name)
                logger.error(f"failed: {script.name} (exit code: {result.returncode})")
        except subprocess.TimeoutExpired:
            failed_scripts.append(script.name)
            logger.error(f"timeout: {script.name} exceeded 1 hour")
        except Exception as e:
            failed_scripts.append(script.name)
            logger.error(f"exception in {script.name}: {e}")

logger.info(f"success: {len(successful_scripts)}, failed: {len(failed_scripts)}")
if failed_scripts:
    logger.error(f"failed scripts: {', '.join(failed_scripts)}")
    exit(1)
