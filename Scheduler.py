from process import Process
from threading import Thread
from Clock import myClock
import logging


class Scheduler(Thread):
    def __init__(
        self,
        number_of_core,
        manager_obj,
        command_obj,
        list_of_processes,
        list_of_threads,
    ):
        super(Scheduler, self).__init__()

        # intialise characteristic
        self.number_of_core = number_of_core
        self.active_processes = []
        self.isFinished = False

        # intialise objects
        self.thread_manager = manager_obj
        self.command_obj = command_obj

        # initialise lists
        self.thread_list = list_of_threads
        self.list_processes = list_of_processes
        self.current_process = []

    def setFinished(self, isFinished):
        self.isFinished = isFinished

    def run(self):
        logger = logging.getLogger(f"{__name__} thread")
        logger.debug("Start  Scheduler Thread")
        while not self.isFinished:
            pass
        logger.debug("Finished  Scheduler Thread")

    def process_thread(self):
        while True:
            if (
                self.list_processes
            ):  # list_process is a list of list that holds all the processes, we are going to see the one at the first index
                self.current_process = self.list_processes[0]
                time_needed_to_start = self.current_process[1]

                if (
                    self.number_of_core > len(self.active_processes)
                    and myClock.time >= time_needed_to_start
                ):

                    new_process = Process(
                        self.thread_manager,
                        self.active_processes,
                        self.command_obj,
                        self.current_process[2],
                        myClock.time,
                        self.current_process[0],
                    )
                    new_process.start()
                    self.active_processes.append(new_process)
                    self.thread_list.append(new_process)
                    self.list_processes.pop(0)

            if len(self.list_processes) == 0:
                if len(self.active_processes) == 0:
                    break
