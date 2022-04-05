from process import Process
from threading import Thread
import logging


class Scheduler(Thread):
    def __init__(
        self,
        number_of_core,
        manager_obj,
        file_output,
        command_obj,
        list_of_processes,
        list_of_threads,
        clock_obj,
    ):
        super(Scheduler, self).__init__()

        # intialise characteristic
        self.number_of_core = number_of_core
        self.active_processes = []
        self.is_finished = False

        # intialise objects
        self.thread_manager = manager_obj
        self.thread_clock = clock_obj
        self.command_obj = command_obj

        # initialise lists
        self.thread_list = list_of_threads
        self.list_processes = list_of_processes
        self.current_process = []

        # output
        self.output_file = file_output

    def set_finished(self, bool1):
        self.is_finished = bool1

    def run(self):
        logger = logging.getLogger(f"{__name__} thread")
        logger.debug("Start  Scheduler Thread")
        while not self.is_finished:
            pass
        logger.debug("Finished  Scheduler Thread")

    def process_thread(self):
        self.thread_clock.start()
        while True:
            if (
                self.list_processes
            ):  # list_process is a list of list that holds all the processes, we are going to see the one at the first index
                self.current_process = self.list_processes[0]
                time_needed_to_start = self.current_process[1]

                if (
                    self.number_of_core > len(self.active_processes)
                    and self.thread_clock.time >= time_needed_to_start
                ):

                    new_process = Process(
                        self.thread_manager,
                        self.thread_clock,
                        self.active_processes,
                        self.command_obj,
                        self.output_file,
                        self.current_process[2],
                        self.thread_clock.time,
                        self.current_process[0],
                    )
                    new_process.start()
                    self.active_processes.append(new_process)
                    self.thread_list.append(new_process)
                    self.list_processes.pop(0)

            if len(self.list_processes) == 0:
                if len(self.active_processes) == 0:
                    break
