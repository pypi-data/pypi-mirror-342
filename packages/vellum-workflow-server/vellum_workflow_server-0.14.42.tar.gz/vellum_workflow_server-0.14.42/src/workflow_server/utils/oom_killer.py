import logging
import multiprocessing
from multiprocessing.synchronize import Event
import os
import signal
from threading import Thread
from time import sleep

from workflow_server.config import MEMORY_LIMIT_MB
from workflow_server.utils.exit_handler import process_killed_switch

logger = logging.getLogger(__name__)

_oom_killed_switch = multiprocessing.Event()

_MAX_MEMORY_PERCENT = 0.97
_WARN_MEMORY_PERCENT = 0.90


def start_oom_killer_worker() -> None:
    logger.info("Starting oom killer watcher...")
    OomKillerThread(kill_switch=_oom_killed_switch).start()


def get_is_oom_killed() -> bool:
    return _oom_killed_switch.is_set()


class OomKillerThread(Thread):
    """
    This worker is for watching for oom errors so we can gracefully kill any workflows in flight
    and tell the user they have a memory limit problem instead of relying on kubernetes to do it
    for us. This currently goes off the max memory not the requested memory so it may not always
    be accurate since max memory may not always be available
    """

    _kill_switch: Event

    def __init__(
        self,
        kill_switch: Event,
    ) -> None:
        Thread.__init__(self)
        self._kill_switch = kill_switch

    def run(self) -> None:
        logger.info("Starting oom watcher...")
        if not MEMORY_LIMIT_MB:
            return

        while True:
            if process_killed_switch.is_set():
                exit(1)
            sleep(2)

            try:
                with open("/sys/fs/cgroup/memory/memory.usage_in_bytes", "r") as file:
                    memory_bytes = file.read()
            except Exception:
                logger.warning("Unable to get current memory.")
                continue

            if not memory_bytes:
                logger.warning("Unable to get current memory.")
                continue

            memory_mb = int(memory_bytes) / 1024 / 1024

            if memory_mb > (MEMORY_LIMIT_MB * _MAX_MEMORY_PERCENT):
                self._kill_switch.set()
                logger.error("Workflow server OOM killed")
                # Give time for the threads to get our kill switch
                sleep(5)
                pid = os.getpid()
                os.kill(pid, signal.SIGKILL)
                exit(1)

            if memory_mb > (MEMORY_LIMIT_MB * _WARN_MEMORY_PERCENT):
                logger.warning("Memory usage exceeded 90% of limit")
