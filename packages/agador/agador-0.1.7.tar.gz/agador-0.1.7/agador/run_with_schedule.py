from .utils import parse_command_map
from .nornir.logging import LOG_FORMAT, DEFAULT_LOGFILE
import logging
import argparse
import sys
import subprocess

from datetime import datetime
import time

logger = logging.getLogger("agador")

LOOP_INTERVAL = 10



def main():
    parser = argparse.ArgumentParser(description="Run agador")
    parser.add_argument("-l", "--log-level", default=logging.INFO, help="Set log level for agador only")
    parser.add_argument("--echo", action="store_true", help="echo logfile to stdout")
    args = parser.parse_args()

    # setting up logging
    file_handler = logging.handlers.RotatingFileHandler(
        DEFAULT_LOGFILE, maxBytes=1024 * 1024 * 10, backupCount=20
    )
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    logger.addHandler(file_handler)
    logger.setLevel(args.log_level)
    if args.echo:
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setFormatter(logging.Formatter(LOG_FORMAT))
        logger.addHandler(stdout_handler)
    
    base_run_cmd = ['python', 'run.py', '-l', args.log_level, '--cmds']

    cmd_map = parse_command_map()
    current_run = None
    
    last_check = datetime.now()
    while True:

        # waiting a bit
        time.sleep(LOOP_INTERVAL)

        # checking the time
        now = datetime.now()

        # if any commands are scheduled to run between now and the last time
        # we checked the time, put them on a list of commands to run
        cmds_to_run = []
        for cmd, data in cmd_map.items():

            run_time = data["frequency"].schedule(now).prev()
            if run_time >= last_check:
                cmds_to_run.append(cmd)

        # If we have commands to run, first check to see if the previous run has completed.
        # if it has, run our new commands
        if cmds_to_run:
            if current_run and current_run.poll() is None:
                logger.error(f"Agador wants to run cmds {','.join(cmds_to_run)} but previous run (PID {current_run.pid}) has not completed!")
            else:
                cmd_args = base_run_cmd.copy()
                cmd_args.extend(cmds_to_run)
                current_run = subprocess.Popen(cmd_args)
                logger.info(f"Starting agador run (PID {current_run.pid}): {cmd_args}")

        last_check = now
        

if __name__ == "__main__":
    main()