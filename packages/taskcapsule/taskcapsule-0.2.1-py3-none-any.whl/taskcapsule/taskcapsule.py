"""
Run tasks concurrently using threads.
"""

import logging
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from threading import Event, Thread
from typing import Any, Callable, Dict, List, Optional

from pydantic import BaseModel

logging.basicConfig()
logger = logging.getLogger("task-runner")
logger.setLevel(level=logging.INFO)

DEFAULT_WORKERS = 10
DEFAULT_SUCCESS = 0
DEFAULT_FAILURE = -1
MONITOR_SLEEP = 2


class TaskException(Exception):
    """
    This exception is to be thrown a Task is misconfigured
    """

    def __init__(self, message="Task is misconfigured"):
        self.message = message
        super().__init__(self.message)


class TaskRunnerException(Exception):
    """
    This exception is to be thrown a TaskRunner encounters an issue outside of trapping the
     called command or function
    """

    def __init__(self, message="TaskRunner encountered an issue"):
        self.message = message
        super().__init__(self.message)


class Task(BaseModel):
    """
    A task to be executed. This class is used to define the command and its arguments.
    It also provides a method to render the command with the given arguments.
    The command uses the string formatting style of Python, where {} is a placeholder for the
    arguments.
    """

    # Only one of these should be set. This is enforced in the model_post_init method
    command: Optional[str] = None
    function: Optional[Callable] = None

    # This isn't strictly necessary for `command` tasks if the command string is rendered when
    # creating the Task object. It is required for `function` Tasks objects where the function
    # is called with the provided arguments.
    kwargs: Optional[Dict[str, Any]] = None
    output_filter: Optional[str] = None
    # use this to pass metatdata to the task which can be used for result collation. This is not
    # used in the task itself.
    target_metadata: Optional[dict] = None

    def model_post_init(self, _context: Any) -> None:

        # Ensure that the task is well defineded.
        if self.command is None and self.function is None:
            raise TaskException("Either command or function must be provided")

        if self.command is not None and self.function is not None:
            raise TaskException("Only command or function must be provided")

    def render_command(self) -> str | None:
        """
        Render the command with the given arguments.
        """
        rendered: str | None = None
        if self.command is not None and self.kwargs is not None:
            expected_args = self.command.count("{")
            provided_args = len(self.kwargs)
            if expected_args == 0:
                logger.warning(
                    "command %s does not contain a placeholder", self.command
                )

            if expected_args != provided_args:
                logger.warning(
                    "command %s has %s placeholders but %s arguments",
                    self.command,
                    expected_args,
                    provided_args,
                )

            if expected_args == provided_args:
                if isinstance(self.kwargs, dict):
                    if isinstance(self.kwargs, dict):
                        rendered = self.command.format(**self.kwargs)
                    else:
                        logger.error("kwargs is not a dictionary, skipping task")
                else:
                    logger.error("kwargs is not a dictionary, skipping task")
        return rendered


class TaskResult(BaseModel):
    """
    A class to store the result of a task. This class is used to store the command, its
    arguments, the return code, the stdout and stderr output, and the duration of the
    task. It also provides methods to check if the task was successful.  Metadata can be passed
    to the task which can be used for result collation.
    """

    command: Optional[str] = None
    function: Optional[str] = None
    kwargs: Optional[Dict[str, Any]] = None
    return_code: int
    output: str
    error: str
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

        return self.success_filter is not None and self.success_filter in self.output


class TaskRunner(BaseModel):
    """
    A class to run tasks in parallel using threads.
    """

    tasks: List[Task]
    workers: int = DEFAULT_WORKERS
    show_failures: bool = False

    # If we want to shoot our own foot, we can set this to False. This will allow us to run tasks
    #  with fewer checks. This is probably a bad idea to disable
    safety: bool = True

    # If we want to monitor the tasks, we can set this to True. This will emit logging messages
    # about progress
    monitoring: bool = True

    def _monitor(self, finished: Event, work_queue: Queue, all_items: int) -> None:
        """

        Monitor the progress of the tasks in the queue. This function is run in a separate thread
        to avoid blocking the main thread.

        :param finished: event to signal when the tasks are finished
        :param work_queue: queue to monitor
        :param all_items: total number of items in the queue
        """
        logger.debug("starting monitor thread")
        while not work_queue.empty() and not finished.is_set():
            logger.info(
                "work assigned: %s/%s",
                all_items - work_queue.qsize(),
                all_items,
            )
            time.sleep(MONITOR_SLEEP)
        logger.info("work assigned: %s/%s", all_items, all_items)
        work_queue.join()
        logger.debug("monitor thread done")

    def worker(self, wid: int, task_queue: Queue):
        """
        Worker function to process items in the queue.
        :param wid: worker id  to identify the worker
        :param queue: queue to process items from
        """
        logger.debug("starting worker-%d", wid)
        while not task_queue.empty():
            task = task_queue.get()
            result = None
            if task.command:
                result = self._run_subprocess(task)
            elif task.function:
                result = self._run_function(task)

            if result is not None:
                if task.target_metadata:
                    result.target_metadata = task.target_metadata

                if task.output_filter:
                    result.success_filter = task.output_filter

                if (
                    result.is_success() or self.show_failures
                ) and result.contains_filter():
                    print(result.model_dump_json(exclude_unset=True))

            task_queue.task_done()

        logger.debug("worker worker-%s done", wid)

    def _run_subprocess(self, task: Task) -> TaskResult | None:
        """
        Run a subprocess with the given command and arguments.

        :param Task: task to run
        :return TaskResult: TaskResult object with the result of the task
        """
        start_time = time.time()
        rendered = task.render_command()
        if rendered is None:
            logger.error("command is None, skipping task")
            return None
        res = None
        try:

            process = subprocess.Popen(
                rendered,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
            )

            stdout, stderr = process.communicate()
            res = TaskResult(
                command=rendered,
                kwargs=task.kwargs,
                return_code=process.returncode,
                output=stdout,
                error=stderr,
                duration=time.time() - start_time,
            )
            return res

        # This will almost always be a subprocess.CalledProcessError, but we catch all exceptions
        #  to avoid crashing the worker thread.
        except Exception as e:  # pylint: disable=broad-except
            logger.error("processing %s: %s", task, e)

            res = TaskResult(
                command=rendered,
                kwargs=task.kwargs,
                return_code=DEFAULT_FAILURE,
                output="",
                error=str(e),
                duration=time.time() - start_time,
            )

        return res

    def _run_function(self, task: Task) -> TaskResult | None:
        start_time = time.time()
        res = None
        if task.function is None:
            logger.error("function is None, skipping task")
            return res
        try:
            if task.kwargs is None:
                result = task.function()
            else:
                result = task.function(**task.kwargs)

            res = TaskResult(
                function=task.function.__name__,
                kwargs=task.kwargs,
                return_code=DEFAULT_SUCCESS,
                output=str(result),
                error="",
                duration=time.time() - start_time,
            )
        except Exception as e:  # pylint: disable=broad-except
            logger.error("processing %s: %s", task, e)
            res = TaskResult(
                function=task.function.__name__,
                kwargs=task.kwargs,
                return_code=DEFAULT_FAILURE,
                output="",
                error=str(e),
                duration=time.time() - start_time,
            )

        return res

    def run(self) -> None:
        """
        Start a thread pool to process items in the queue.
        :param items: list of items to process
        """
        worker_queue: Queue = Queue()

        # Don't overspawn workers
        num_workers = min(self.workers, len(self.tasks))
        logger.info("spawning %s workers", num_workers)
        with ThreadPoolExecutor(max_workers=num_workers) as controller:
            # load the queue before starting the workers to avoid worker starvation and exiting
            for t in self.tasks:
                worker_queue.put(t)

            finished = Event()
            monitor = Thread(
                target=self._monitor,
                args=(
                    finished,
                    worker_queue,
                    len(self.tasks),
                ),
            )
            monitor.start()

            for wid in range(num_workers):
                controller.submit(self.worker, wid, worker_queue)

            logger.debug("joining queue")
            worker_queue.join()
            finished.set()

            # wait for the monitor thread to finish
            time.sleep(MONITOR_SLEEP)
            logger.info("all tasks completed")
