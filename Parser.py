from Commands import Commands
from Page import Page
from Main_Memory import Main_Memory
from Clock import clock


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
            [
                process_number,
                int(p.split(" ")[0]),
                int(p.split(" ")[1].rstrip()),
            ]
        )
        process_number += 1

    process = sorted(process, key=lambda item: item[1])

    print(process)

    # MEMCONFIG.TXT
    with open("memconfig.txt", mode="r") as mem:
        input_lines2 = mem.readlines()
        # number of pages in main memory
        number_of_pages = int(input_lines2[0])

    # COMMANDS.TXT
    with open("commands.txt", "r") as com:
        commands = com.readlines()
        list_of_commands = []
        for command in commands:
            line_split = command.split()
            if len(line_split) == 2:
                list_of_commands.append([line_split[0], line_split[1]])
            elif len(line_split) == 3:
                list_of_commands.append(
                    [line_split[0], line_split[1], line_split[2]]
                )
        print(list_of_commands)

    return (
        process,
        number_of_pages,
        number_of_core,
        list_of_commands,
    )


def object_creations(list_of_commands, number_of_pages):
    command_object = Commands(list_of_commands)
    disk_object = Page()
    thread_clock = clock()
    memory_object = Main_Memory(number_of_pages)
    return command_object, disk_object, thread_clock, memory_object
