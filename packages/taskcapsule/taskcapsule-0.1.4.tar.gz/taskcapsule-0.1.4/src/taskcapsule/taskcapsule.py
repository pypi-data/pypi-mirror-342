"""
Run tasks in parallel using threads. This is a simple task runner that uses threads to run
tasks in parallel.
"""

import logging
import queue
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

logging.basicConfig()
logger = logging.getLogger("task-runner")
logger.setLevel(level=logging.INFO)

DEFAULT_WORKERS = 10


class Task(BaseModel):
    """
    A task to be executed. This class is used to define the command and its arguments.
    It also provides a method to render the command with the given arguments.
    The command uses the string formatting style of Python, where {} is a placeholder for the
    arguments.
    """

    command: str
    kwargs: Dict[str, Any]
    output_filter: Optional[str] = None
    # use this to pass metatdata to the task which can be used for result collation. This is not
    # used in the task itself.
    target_metadata: Optional[dict] = None

    def render_command(self) -> str | None:
        """
        Render the command with the given arguments.
        """
        rendered: str | None = None
        expected_args = self.command.count("{")
        provided_args = len(self.kwargs)
        if expected_args == 0:
            logger.warning("command %s does not contain a placeholder", self.command)

        if expected_args != provided_args:
            logger.warning(
                "command %s has %s placeholders but %s arguments",
                self.command,
                expected_args,
                provided_args,
            )

        if expected_args == provided_args:
            rendered = self.command.format(**self.kwargs)
        return rendered


class TaskResult(BaseModel):
    """
    A class to store the result of a task. This class is used to store the command, its
    arguments, the return code, the stdout and stderr output, and the duration of the
    task. It also provides methods to check if the task was successful.  Metadata can be passed
    to the task which can be used for result collation.
    """

    command: str
    kwargs: Dict[str, Any]
    return_code: int
    stdout: str
    stderr: str
    duration: float
    success_filter: Optional[str] = None
    target_metadata: Optional[dict] = None

    def is_success(self) -> bool:
        """
        Check if the job was successful based on the return code. POSIX standards define success
         as a return code of 0.
        :return: True if the job was successful, False otherwise.
        """
        return self.return_code == 0

    def contains_filter(self) -> bool:
        """
        Check if the job output contains the success filter.
        :return: True if the job output contains the success filter, False otherwise.
        """
        if self.success_filter is None:
            logger.info("success filter is None, skipping check")
            return True

        return self.success_filter is not None and self.success_filter in self.stdout


class TaskRunner(BaseModel):
    """
    A class to run tasks in parallel using threads.
    """

    tasks: List[Task]
    workers: int = DEFAULT_WORKERS

    def worker(self, wid: int, task_queue: queue.Queue):
        """
        Worker function to process items in the queue.
        :param wid: worker id  to identify the worker
        :param queue: queue to process items from
        """
        logger.debug("starting worker-%d", wid)
        while not task_queue.empty():
            task = task_queue.get()
            rendered = task.render_command()
            try:
                logger.debug("worker-%d working on %s", wid, rendered)
                start_time = time.time()

                process = subprocess.Popen(
                    rendered,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True,
                )

                stdout, stderr = process.communicate()
                duration = time.time() - start_time

                # Store results
                result = TaskResult(
                    command=task.render_command(),
                    kwargs=task.kwargs,
                    return_code=process.returncode,
                    stdout=stdout,
                    stderr=stderr,
                    duration=duration,
                )

                if task.target_metadata:
                    result.target_metadata = task.target_metadata

                if task.output_filter:
                    result.success_filter = task.output_filter

                if result.is_success() and result.contains_filter():
                    print(result.model_dump_json())

            # No idea what is being run in the subprocess, so catch all exceptions
            except Exception as e:  # pylint: disable=broad-except
                logger.error("worker-%s error processing %s: %s", wid, task, e)

            finally:
                task_queue.task_done()

            if task is None:
                task_queue.task_done()

        logger.debug("worker worker-%s done", wid)

    def run(self) -> None:
        """
        Start a thread pool to process items in the queue.
        :param items: list of items to process
        """
        worker_queue: queue.Queue = queue.Queue()

        # Don't overspawn workers
        num_workers = min(self.workers, len(self.tasks))
        logger.info("spawning %s workers", num_workers)
        with ThreadPoolExecutor(max_workers=num_workers) as controller:
            for t in self.tasks:
                worker_queue.put(t)

            for wid in range(num_workers):
                controller.submit(self.worker, wid, worker_queue)

            logger.debug("joining queue")
            worker_queue.join()
            logger.info("all tasks completed")
