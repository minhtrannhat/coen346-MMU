from Commands import Commands
from Page import Page
import logging
from VirtualMemory import VirtualMemory

logger = logging.getLogger(f"{__name__} thread")


def extract_data():

    # Process processes
    with open("processes.txt", mode="r") as process:
        lines = process.readlines()
        numberOfCores = int(lines[0])
        numberOfProcesses = int(lines[1])

    listOfProcesses = []
    processNumber = 1

    for process in lines[2:]:
        listOfProcesses.append(
            [
                processNumber,
                int(process.split(" ")[0]),
                int(process.split(" ")[1].rstrip()),
            ]
        )
        processNumber += 1

    # sort all processes
    logger.debug(f"List of all processes before sorting: {listOfProcesses}")
    listOfProcesses = sorted(listOfProcesses, key=lambda item: item[1])
    logger.debug(f"List of all processes after sorting: {listOfProcesses}")

    # process memonfig.txt
    with open("memconfig.txt", mode="r") as file:
        lines = file.readlines()
        numberOfPages = int(lines[0])
        K_VALUE = int(lines[1])
        timeOut = int(lines[2])

        logger.debug(f"Number of pages is: {numberOfPages}")
        logger.debug(f"The K value is: {K_VALUE}")
        logger.debug(f"The time out value is {timeOut}")

    # COMMANDS.TXT
    with open("commands.txt", "r") as file:
        lines = file.readlines()
        listOfCommands = []
        for line in lines:
            line_split = line.split()
            if len(line_split) == 2:
                listOfCommands.append([line_split[0], line_split[1]])
            elif len(line_split) == 3:
                listOfCommands.append(
                    [line_split[0], line_split[1], line_split[2]]
                )
        logger.debug(f"List of commands: {listOfCommands}")

    return (
        listOfProcesses,
        numberOfPages,
        numberOfCores,
        listOfCommands,
    )


def object_creations(listOfCommands, numberOfPages):
    commandObject = Commands(listOfCommands)
    diskObject = Page()
    memoryObject = VirtualMemory(numberOfPages)
    return commandObject, diskObject, memoryObject
