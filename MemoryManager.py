from threading import Thread, Lock
import logging


class MemoryManager(Thread):
    def __init__(self, clock, cmd_obj, output_file, disk_page, memory):
        super(MemoryManager, self).__init__()
        self.isFinished = False

        # Creating necessary objects needed
        # We will need an memory object in order to write to the virtual memory and append to it
        # we will need a command object in order to know which command to run at the present time
        # we will need the thread clock because we are keeping track of the time
        # we will need a disk page because in order to know which command to run at the present time

        self.object_memory = memory
        self.object_command = cmd_obj
        self.thread_clock = clock
        self.page_disk = disk_page

        # Semaphores
        self.lock = Lock()

        # initialize output file
        self.output_file = output_file

    def set_finished(self, isFinished: bool):
        self.isFinished = isFinished

    def run(self):
        logger = logging.getLogger(f"{__name__} thread")
        logger.debug("Starting Memory Manager Thread")
        while not self.isFinished:
            pass
        logger.debug("Exiting Memory Manager Thread")

    def store_function(self, Id, Value):
        if not self.object_memory.full():
            self.object_memory.add_to_main_memory(Id, Value)
        else:
            self.page_disk.Write([Id, Value])

    def look_up_function(self, Id):
        if self.object_memory.get_variable(Id) == -1:
            return self.swap(Id)
        return self.object_memory.get_variable(Id)

    def release_function(self, Id):
        self.object_memory.release(Id)

    def swap(self, Id):
        logger = logging.getLogger(f"{__name__} thread")
        # For this swap to work, we should basically perform the principle of a bubble sort with the temp values
        temporary_index_value = int(self.object_memory.Index_LRU())
        logger.debug(f"temporary_index_value is {temporary_index_value}")
        temporary_memory = self.object_memory.memory[temporary_index_value]
        logger.debug(f"temp_memory currently is {temporary_memory}")
        temporary_disk = self.page_disk.read(Id)
        # We will make use of the functions set and write that were defined in the virtual memory and in the disk classes . Those were written for that purpose precisely

        self.object_memory.set_page(temporary_index_value, temporary_disk)
        self.page_disk.Write(temporary_memory)

        logger.info(
            f"Clock: {self.thread_clock.time},  Memory Manager Swap: Variable {Id} with Variable {temporary_memory[temporary_index_value]}"
        )
        return temporary_disk[1]

    def api(self, object_command, process_number, term_time):
        logger = logging.getLogger(f"{__name__} thread")
        with self.lock:
            if len(object_command) > 2:
                com = object_command[0]
                com1 = object_command[1]
                com2 = object_command[2]
                Id = com1
            else:
                com = object_command[0]
                com1 = object_command[1]
                Id = com1
            if com == "Release":
                self.release_function(com1)
                logger.info(
                    f"Clock: {self.thread_clock.time}, Process {process_number}: {com}: Variable: {Id}"
                )

            elif com == "Store":
                self.status = True
                self.store_function(com1, com2)
                logger.info(
                    f"Clock: {self.thread_clock.time}, Process {process_number}: {com}: Variable {Id}, Value: {com2}"
                )
                self.status = False

            elif com == "Lookup":
                self.thread_clock.add_time(10)
                self.look_up_function(com1)
                logger.info(
                    f"Clock: {self.thread_clock.time}, Process {process_number}: {com}: Variable {Id}, Value: {self.object_memory.get_variable(Id)}"
                )
