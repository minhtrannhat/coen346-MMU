from Clock import clock
from Coms import Commands
from Pages import Page
from process import Process
from Scheduler import Scheduler
from Main_Memory import Main_Memory
from MemoryManager import MemoryManager


def extract_data():

    # PROCESS TEXT FILE
    with open("processes.txt", mode="r") as pro:
        input_lines = pro.readlines()
        # print(input_lines)
        # First line represent the number of cores
        number_of_core = int(input_lines[0])
        # Second line represent the number of N processes
        number_of_processes = int(input_lines[1])
    # Rest of the file we need a list of process start time and duration, each element of the list represent a process with its number, its ready time and its service time

    process = []
    process_number = 1
    for p in input_lines[2:]:

        process.append(
            [process_number, int(p.split(" ")[0]), int(p.split(" ")[1].rstrip())]
        )
        process_number += 1

    process = sorted(process, key=lambda item: item[1])

    print(process)

    # MEMCONFIG.TXT
    with open("memconfig.txt", mode="r") as mem:
        input_lines2 = mem.readlines()
        # this file represents the number of pages in main memory
        number_of_pages = int(input_lines2[0])

    # COMMANDS.TXT ########
    with open("commands.txt", "r") as com:
        commands = com.readlines()
        # list_of_commands represent a list of lis
        list_of_command = []
        for c in commands:
            line_split = c.split()
            if len(line_split) == 2:
                list_of_command.append([line_split[0], line_split[1]])
            elif len(line_split) == 3:
                list_of_command.append([line_split[0], line_split[1], line_split[2]])
        print(list_of_command)

    return (
        process,
        number_of_pages,
        number_of_core,
        number_of_processes,
        list_of_command,
    )


def object_creations(list_of_command, number_of_pages):
    command_object = Commands(list_of_command)
    disk_object = Page()
    thread_clock = clock()
    memory_object = Main_Memory(number_of_pages)
    return command_object, disk_object, thread_clock, memory_object


def main():

    list_of_threads = (
        []
    )  # containing them in a list will allow us to track them and join
    (
        processes,
        number_of_pages,
        number_of_cores,
        number_of_processes,
        list_of_command,
    ) = extract_data()

    command_object, disk_object, thread_clock, memory_object = object_creations(
        list_of_command, number_of_pages
    )

    output = "output.txt"

    thread_manager = MemoryManager(
        thread_clock, command_object, output, disk_object, memory_object
    )
    thread_manager.start()

    thread_scheduler = Scheduler(
        number_of_cores,
        thread_manager,
        output,
        command_object,
        processes,
        list_of_threads,
        thread_clock,
    )
    thread_scheduler.start()

    list_of_threads.append(thread_clock)
    list_of_threads.append(thread_manager)
    list_of_threads.append(thread_scheduler)

    thread_scheduler.process_thread()

    for threads in list_of_threads:
        threads.set_finished(True)
        threads.join()

    print("Virtual Memory : ")
    print(memory_object.memory)


if __name__ == "__main__":
    main()
