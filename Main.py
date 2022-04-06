from Scheduler import Scheduler
from MemoryManager import MemoryManager
from Parser import extract_data, object_creations
from Clock import myClock
import logging


def main():
    # setup logging to output.txt
    logging.basicConfig(
        filename="output.txt",
        filemode="w",
        force=True,
        level=logging.INFO,
        format="{message}",
        style="{",
    )

    logger = logging.getLogger(__name__)

    listOfThreads = []

    (
        listOfProcesses,
        numberOfPages,
        numberOfCores,
        listOfCommands,
    ) = extract_data()

    (
        commands,
        diskObject,
        memoryObject,
    ) = object_creations(listOfCommands, numberOfPages)

    # start the clock
    myClock.start()

    # start the MMU
    memoryManager = MemoryManager(commands, diskObject, memoryObject)
    memoryManager.start()

    # initialise and start the Scheduler
    scheduler = Scheduler(
        numberOfCores,
        memoryManager,
        commands,
        listOfProcesses,
        listOfThreads,
    )
    scheduler.start()

    listOfThreads.append(memoryManager)
    listOfThreads.append(scheduler)

    scheduler.process_thread()

    for thread in listOfThreads:
        thread.set_finished(True)
        thread.join()

    myClock.join()

    logger.debug(f"Memory: {memoryObject.memory}")


if __name__ == "__main__":
    main()
