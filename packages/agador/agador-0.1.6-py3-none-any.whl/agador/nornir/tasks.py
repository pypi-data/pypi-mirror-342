import logging
import traceback
from nornir.core.task import Result, Task
from nornir.core.exceptions import NornirSubTaskError
from sqlalchemy.engine import Engine

from umnet_napalm import get_network_driver

from ..utils import get_device_cmd_list
from ..mappers.save_to_file import SaveResult
from ..mappers.save_to_db import ResultsToDb

from .nornir_setup import NUM_WORKERS
from sqlalchemy import create_engine

logger = logging.getLogger(__name__)


def process_device(
    task: Task,
    cmd_list: list,
    cmd_map: dict,
    db_url:str,
) -> Result:
    """
    Run a set of commands against a specific device based on the
    command mapper and an optional restricted list of commands.
    If no list is provided all commands in the mapper will be run
    """
    logger.debug(f"In process device task for {task.host}")
    failed = False
    db_engine = create_engine(
        db_url, pool_size=NUM_WORKERS, max_overflow=NUM_WORKERS + 10
    )
    # first figure out which commands to run against this host
    cmd_list = get_device_cmd_list(cmd_map, task.host, cmd_list_filter=cmd_list)

    logger.info(f"Running getters on {task.host.name}: {cmd_list}")
    if not cmd_list:
        logger.info(f"No commands to execute for {task.host.name}")
        return Result(host=task.host, result="No commands to execute")

    # finding that for multiprocessing it's cleaner to use the context
    # manager - by this we mean 'with network_driver as device' - because
    # connection failures that raise exceptions aren't well tolerated.
    network_driver = get_network_driver(task.host.platform)
    parameters = {
        "hostname": task.host.hostname,
        "username": task.host.username,
        "password": task.host.password,
        "optional_args": {},
    }
    parameters.update(task.host.connection_options["umnet_napalm"].extras)

    getter_results = {}
    try:
        with network_driver(**parameters) as device:

            for cmd, options in cmd_list.items():
                method = getattr(device, cmd_map[cmd]["getter"])
                getter_results[cmd] = method(**options)

    except Exception as e:
        tb = traceback.format_exc()
        logger.error(
            "Host %r getters failed with traceback:\n%s",
            task.host.name,
            tb,
        )
        return Result(host=task.host, result=tb, error=str(e), failed=True)

    # for each command save data using the appropriate methods based
    # on the command map
    for cmd, result in getter_results.items():

        if "save_to_db" in cmd_map[cmd]:
            try:
                task.run(
                    name=f"{cmd}_save_to_db",
                    task=update_table,
                    result=result,
                    engine=db_engine,
                    mapper=cmd_map[cmd]["save_to_db"],
                )
            except NornirSubTaskError:
                failed = True

        if "save_to_file" in cmd_map[cmd]:
            try:
                task.run(
                    name=f"{cmd}_save_to_file",
                    task=save_to_file,
                    result=result,
                    repo_path=cmd_map[cmd]["save_to_file"]["destination"],
                    mapper=cmd_map[cmd]["save_to_file"]["mapper"],
                )
            except NornirSubTaskError:
                failed = True

    return Result(host=task.host, result="Completed", failed=failed)


def update_table(
    task: Task,
    result: Result,
    engine: Engine,
    mapper: ResultsToDb,
) -> Result:
    """
    Generic task for taking the results from a previous "napalm_get"
    task and saving it to the database
    """
    mapper(task.host.name, task.host.hostname, result, engine)

    return Result(host=task.host)


def save_to_file(
    task: Task,
    result: dict,
    repo_path: str,
    mapper: SaveResult,
) -> Result:
    """
    Task for saving to a file
    """
    mapper(task.host, repo_path, result)

    return Result(host=task.host)
