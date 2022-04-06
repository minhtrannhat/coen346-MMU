from threading import Thread, Lock
import logging
from Clock import myClock


class MemoryManager(Thread):
    def __init__(self, commands, diskSpace, virtualMemory):
        super(MemoryManager, self).__init__()
        self.isFinished = False
        self.virtualMemory = virtualMemory
        self.commands = commands
        self.diskSpace = diskSpace

        # Semaphores
        self.lock = Lock()

    def set_finished(self, isFinished: bool):
        self.isFinished = isFinished

    def run(self):
        logger = logging.getLogger(f"{__name__} thread")
        logger.debug("Starting Memory Manager Thread")
        while not self.isFinished:
            pass
        logger.debug("Exiting Memory Manager Thread")

    def store_function(self, Id, Value):
        if not self.virtualMemory.full():
            self.virtualMemory.add_to_main_memory(Id, Value)
        else:
            self.diskSpace.Write([Id, Value])

    def look_up_function(self, Id):
        if self.virtualMemory.get_variable(Id) == -1:
            return self.swap(Id)
        return self.virtualMemory.get_variable(Id)

    def release_function(self, Id):
        self.virtualMemory.release(Id)

    def swap(self, Id):
        currentTime: int = myClock.time
        logger = logging.getLogger(f"{__name__} thread")
        # For this swap to work, we should basically perform the principle of a bubble sort with the temp values
        temporary_index_value = int(self.virtualMemory.Index_LRU())
        logger.debug(f"temporary_index_value is {temporary_index_value}")
        temporary_memory = self.virtualMemory.memory[temporary_index_value]
        logger.debug(f"temp_memory currently is {temporary_memory}")
        temporary_disk = self.diskSpace.read(Id)
        # We will make use of the functions set and write that were defined in the virtual memory and in the disk classes . Those were written for that purpose precisely

        self.virtualMemory.set_page(temporary_index_value, temporary_disk)
        self.diskSpace.Write(temporary_memory)

        logger.info(
            f"Clock: {currentTime}, Memory Manager Swap: Variable {Id} with Variable {temporary_memory[temporary_index_value]}"
        )
        return temporary_disk[1]

    def api(self, commands, process_number, term_time):
        logger = logging.getLogger(f"{__name__} thread")

        currentTime: int = myClock.time

        with self.lock:
            if len(commands) > 2:
                com = commands[0]
                com1 = commands[1]
                com2 = commands[2]
                Id = com1

                if com == "Store":
                    self.status = True
                    self.store_function(com1, com2)
                    logger.info(
                        f"Clock: {currentTime}, Process {process_number}: {com}: Variable {Id}, Value: {com2}"
                    )
                    self.status = False
            else:
                com = commands[0]
                com1 = commands[1]
                Id = com1

                if com == "Release":
                    self.release_function(com1)
                    logger.info(
                        f"Clock: {currentTime}, Process {process_number}: {com}: Variable: {Id}"
                    )

                elif com == "Lookup":
                    myClock.add_time(10)
                    self.look_up_function(com1)
                    logger.info(
                        f"Clock: {currentTime}, Process {process_number}: {com}: Variable {Id}, Value: {self.virtualMemory.get_variable(Id)}"
                    )
