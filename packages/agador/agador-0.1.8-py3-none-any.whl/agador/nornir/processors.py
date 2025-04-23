import logging
import threading
from datetime import datetime
from email.message import EmailMessage
import smtplib

from nornir.core.task import AggregatedResult, Task, MultiResult
from nornir.core.inventory import Host

from .logging import LOG_FORMAT, ThreadLogFilter

class ProcessorBase:
    """
    convenience parent class so we don't have to define unused
    methods in child classes
    """


    def task_started(self, task: Task) -> None:
        pass

    def task_completed(self, task: Task, result: AggregatedResult) -> None:
        pass

    def task_instance_started(self, task: Task, host: Host) -> None:
        pass

    def task_instance_completed(
        self, task: Task, host: Host, result: MultiResult
    ) -> None:
        pass

    def subtask_instance_started(self, task: Task, host: Host) -> None:
        pass

    def subtask_instance_completed(
        self, task: Task, host: Host, result: MultiResult
    ) -> None:
        pass


    
class AgadorProcessor(ProcessorBase):
    """
    Agador processor. Designed to write to a specified logfile and optionally to stdout.
    Will send an email summarizing the results at the end.
    """
    def __init__(self, total_hosts:int, email_from:str, email_to:str, logfile:str, cli_output:bool=False):
        self.total_hosts=total_hosts
        self.email_from = email_from
        self.email_to=email_to
        self.logfile=logfile
        self.cli_output=cli_output
        self.start_time = datetime.now()

    def _log_output(self, output_str:str):
        
        with open(self.logfile, "a", encoding="utf-8") as fh:
            fh.write(output_str)
        
        if self.cli_output:
            print(output_str)

    def task_started(self, task: Task) -> None:
        msg = f"\n******* {task.name} Started at {self.start_time} *******\n"
        self._log_output(msg)
    

    def task_instance_completed(
        self, task: Task, host: Host, result: MultiResult
    ) -> None:

        msg = f"** {host.name} "
        if result.failed:
            msg += f"failed at {datetime.now()}"
            for r in result:
                if r.exception:
                    msg += f" and raised an exception {r.exception}"
                if r.result:
                    msg += f" with traceback:\n\n{r.result}\n\n"

            msg += "**"
        else:
            msg += f"completed successfully at {datetime.now()}"

        msg += "**\n"
        self._log_output(msg)

    def task_completed(self, task: Task, result: AggregatedResult) -> None:
        """
        going to log, optionally print, and email the final results
        """
        # calculating how long the run took
        now = datetime.now()
        elapsed = (now - self.start_time).seconds
        m, s = divmod(elapsed, 60)
        h, m = divmod(m, 60)
        duration = f"{h} hours, {m} minutes, {s}, seconds"

        # generating outpupt message
        num_failed = len([r for r in result.values() if r.failed])
        num_passed = self.total_hosts - num_failed

        result_str = f"Completed run against {self.total_hosts} devices at {now}\n\n"
        result_str += f"Elapsed time: {duration}\nTotal passed: {num_passed}\nTotal failed {num_failed}\n"

        if num_failed:
            result_str += "\nThe following devices failed the following tasks:\n"
            for device, multi_results in result.items():
                failed_tasks = [r.name for r in multi_results if r.failed]
                if failed_tasks:
                    result_str += f"\t{device}: {','.join(failed_tasks)}\n"

        # log and optionalluy 
        self._log_output(result_str)

        msg = EmailMessage()
        msg["Subject"] = f"Run result at {now}"
        msg["From"] = self.email_from
        msg["To"] = self.email_to
        msg.set_content(result_str)

        with smtplib.SMTP("localhost") as s:
            s.send_message(msg)

# # pylint: disable=missing-function-docstring
# class PrintResults(ProcessorBase):
#     """
#     Basic CLI printer of results - every 10 hosts that are completed
#     generates a progress message. At the end results for each host are printed

#     Reference https://nornir.readthedocs.io/en/latest/tutorial/processors.html
#     """

#     def __init__(self, total_hosts: int):

#         self.total = total_hosts
#         self.completed = 0
#         self.passed = 0
#         self.failed = 0

#         print(f"***** Starting run at {self.start_time} *******")

#     def task_started(self, task: Task) -> None:
#         print(f"****** Starting {task.name} *******")

#     def task_completed(self, task: Task, result: AggregatedResult) -> None:

#         elapsed = datetime.now() - self._start_time
#         hours, remainder = divmod(elapsed.seconds, 3600)
#         mins, seconds = divmod(remainder, 60)

#         print(
#             f"****** {task.name} Completed after {hours} hours, {mins} mins, {seconds} seconds *********"
#         )
#         for device, multi_results in result.items():
#             failed_tasks = [r.name for r in multi_results if r.failed]
#             if failed_tasks:
#                 print(f"\t{device}: FAILED {','.join(failed_tasks)}")
#             # else:
#             #    print(f"\t{device}: PASSED")

#     def task_instance_completed(
#         self, task: Task, host: Host, result: MultiResult
#     ) -> None:
#         if result.failed:
#             print(f"\t{host.name} completed - FAILED")
#         else:
#             print(f"\t{host.name} completed - PASSED")


# class LogResults(ProcessorBase):

#     def __init__(self, logfile: str):
#         self.logfile = logfile

#     def task_started(self, task: Task) -> None:
#         with open(self.logfile, "a", encoding="utf-8") as fh:
#             fh.write(f"\n******* {task.name} Started at {datetime.now()} *******\n")

#     def task_instance_started(self, task: Task, host: Host) -> None:
#         with open(self.logfile, "a", encoding="utf-8") as fh:
#             fh.write(f"**{host.name} {task.name} started at {datetime.now()} **\n")

#     def task_instance_completed(
#         self, task: Task, host: Host, result: MultiResult
#     ) -> None:

#         msg = f"** {host.name} "
#         if result.failed:
#             msg += f"failed at {datetime.now()}"
#             for r in result:
#                 if r.exception:
#                     msg += f" and raised an exception {r.exception}"
#                 if r.result:
#                     msg += f" with traceback:\n\n{r.result}\n\n"

#             msg += "**"
#         else:
#             msg += f"completed successfully at {datetime.now()}"

#         msg += "**\n"

#         with open(self.logfile, "a", encoding="utf-8") as fh:
#             fh.write(msg)

#     def task_completed(self, task: Task, result: AggregatedResult) -> None:

#         with open(self.logfile, "a", encoding="utf-8") as fh:
#             fh.write(_get_result_summary(task, result))


# class EmailResults(ProcessorBase):

#     def __init__(self, from_email: str, to_email: str):
#         self.from_email = from_email
#         self.to_email = to_email


#     def task_completed(self, task: Task, result: AggregatedResult) -> None:

#         timestamp = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
#         msg = EmailMessage()
#         msg["Subject"] = f"Run result at {timestamp}"
#         msg["From"] = self.from_email
#         msg["To"] = self.to_email
#         msg.set_content(_get_result_summary(task, result))

#         with smtplib.SMTP("localhost") as s:
#             s.send_message(msg)


class TraceFile(ProcessorBase):
    """
    Class that sets up and tears down logging to a host-based tracefile
    """

    def __init__(self, trace_dir: str):
        self.trace_dir = trace_dir

    def task_instance_started(self, task: Task, host: Host) -> None:
        """
        Sets up tracefile and log handler filtering for the host's thread name
        """
        thread_name = threading.current_thread().name
        timestamp = datetime.now().strftime("%Y%d%m_%H%M%S")

        log_file = f"{self.trace_dir}/{host.name}_{timestamp}.trace"
        log_handler = logging.FileHandler(log_file)
        log_handler.addFilter(ThreadLogFilter(thread_name))
        log_handler.setFormatter(logging.Formatter(LOG_FORMAT))
        log_handler.name = host.name

        logger = logging.getLogger()
        logger.addHandler(log_handler)
        logger.setLevel(logging.DEBUG)

    def task_instance_completed(
        self, task: Task, host: Host, result: MultiResult
    ) -> None:
        """
        Tears down host log filter so that hosts using the same thread
        in the future don't get logged to this file
        """
        logger = logging.getLogger()

        # should only be one with this name
        [logger.removeHandler(h) for h in logger.handlers if h.name == task.host.name]
