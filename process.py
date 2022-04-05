import random  # we need to import random since the assignment said the time was random
from threading import Thread, Lock  # for threading
from time import sleep  # for time purposes import logging
import logging


class Process(Thread):
    # Change order later
    def __init__(
        self,
        manager_obj,
        clock_obj,
        current_processes,
        command_obj,
        output_file,
        service_times,
        S_Time,
        process_numbers,
    ):
        super(Process, self).__init__()
        # setting the processes caracteristics
        self.process_status = False
        self.process_number = process_numbers
        # initialising classes object
        self.thread_clock = clock_obj
        self.thread_manager = manager_obj
        self.theard_command = command_obj

        # initialising time caracteristics
        self.starting_time = S_Time
        self.service_time = service_times
        self.end_time = self.starting_time + self.service_time

        # initialising threading components // lock
        self.lock = Lock()
        self.active_processes = current_processes

        # output file
        self.output1 = output_file

    def set_finished(self, bool1):
        self.process_status = bool1

    def run(self):
        logger = logging.getLogger(f"{__name__} thread")

        logger.info(
            f"Clock: {self.starting_time}, Process {self.process_number}: Start"
        )

        while self.end_time > self.thread_clock.time:
            self.execute()

        logger.info(
            f"Clock: {self.end_time}, Process {self.process_number}: Finished"
        )

        for proces in self.active_processes:
            if proces.process_number == self.process_number:
                self.active_processes.remove(proces)
                break

        logger.debug(f"Exit Process {self.process_number} Thread")

    def execute(self):
        # controlling accesses to shared ressources , it will prevent against corruption of data
        with self.lock:
            wait_time = (
                min(
                    self.end_time - self.thread_clock.time,
                    random.randrange(0, 1000),
                )
                / 1000
            )
            if wait_time > 0:

                sleep(wait_time)

                if self.end_time - self.thread_clock.time > 300:
                    command = self.theard_command.list[
                        self.theard_command.index
                    ]
                    self.theard_command.next_cmd()
                    self.thread_manager.api(
                        command,
                        self.process_number,
                        self.end_time,
                    )

            else:
                self.process_status = True
