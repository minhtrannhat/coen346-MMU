from Scheduler import Scheduler
from MemoryManager import MemoryManager
from Parser import extract_data, object_creations
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

    list_of_threads = []
    (
        processes,
        number_of_pages,
        number_of_cores,
        list_of_command,
    ) = extract_data()

    (
        command_object,
        disk_object,
        thread_clock,
        memory_object,
    ) = object_creations(list_of_command, number_of_pages)

    output = "output.txt"

    memoryManager = MemoryManager(
        thread_clock, command_object, output, disk_object, memory_object
    )
    memoryManager.start()

    thread_scheduler = Scheduler(
        number_of_cores,
        memoryManager,
        output,
        command_object,
        processes,
        list_of_threads,
        thread_clock,
    )
    thread_scheduler.start()

    list_of_threads.append(thread_clock)
    list_of_threads.append(memoryManager)
    list_of_threads.append(thread_scheduler)

    thread_scheduler.process_thread()

    for thread in list_of_threads:
        thread.set_finished(True)
        thread.join()

    logger.debug(f"Memory: {memory_object.memory}")


if __name__ == "__main__":
    main()
