from Page import Page
import logging
from pathlib import Path

logger = logging.getLogger(f"{__name__}")


class Diskspace:
    def __init__(self):
        filename = Path("vm.txt")
        filename.touch(exist_ok=True)

    def write(self, page: Page):
        with open("vm.txt", mode="r+") as file:
            # change if the page is already on the disk
            lines = file.readlines()
            for i, line in enumerate(lines):
                if line == page:
                    self.change(page, i)
                    logger.debug("Modifying a line in disk space")
                    return
            self.add(page)

    def change(self, page: Page, index):
        with open("vm.txt", mode="r+") as file:
            lines = file.readlines()

        lines[index] = "(" + str(page.ID) + "," + str(page.value) + ")" + "\n"
        logger.debug(f"Line to be changed in disk space: {lines[index]}")
        with open("vm.txt", mode="w+") as rep:
            rep.writelines(lines)

        # return the ID and Value of the page that is no longer in disk space
        return int(lines[index].strip()[1]), int(lines[index].strip()[3])

    def read(self, id: int):
        with open("vm.txt", mode="r+") as vm:
            lines = vm.readlines()
            for line in lines:
                if line.strip()[0] == id:
                    logger.debug(f"Found page with ID: {id} in disk space")
                    return line
        logger.debug(f"Can't find page with ID: {id} in disk space")
        return -1

    def add(self, page: Page):
        with open("vm.txt", mode="a+") as vm1:
            logger.debug(f"Appending page {page} to disk space")
            vm1.write("(" + str(page.ID) + "," + str(page.value) + ")" + "\n")
