# the page class represent the VM.TXT file.
# Basically, this text needed to be considered as an array,
# when there was no more space in the virtual memory used
# in the assignment(which was 2 ),
#  we needed to write to the vm.txt This class allowed us
#  to handle this .txt with different functions


class Page:
    def __init__(self):
        pass

    # we needed a function that was able to write to the page object
    # This Write function , will take as an argument the page we want to write into the vm as a form of an array [Id,Value]
    # To write, we input the txt file, we loop through each line and we add to the page if the variable dosnt already exist
    def Write(self, array_page):
        with open("vm.txt", mode="r") as f:
            input_line = f.readlines()
            for i, lines in enumerate(input_line):
                if lines[0] == array_page[0]:
                    self.change(input_line, array_page, i)
                    return
            self.add(array_page)

    # this function is called by the write function when the id is already found in the vm at a certain index
    # it takes input line which is the input that comes from the read of the write. Since we know at what index it was found, we look at the list at that index and we modify it

    def change(self, input_line, array_page, index):
        input_line[index] = str(array_page[0]) + " " + str(array_page[1] + "\n")
        with open("vm.txt", mode="w") as rep:
            rep.writelines(input_line)

    # this read function, reads the vm, loop through each line and if the id is found we return at which line that id was found

    def read(self, Id):
        with open("vm.txt", mode="r") as vm:
            input_line2 = vm.readlines()
            for line in input_line2:
                if str(Id) == line[0]:
                    return line
        return -1

    # this add function is used to add a new line to the vm, we dont need to loop as we already looped in the write function.

    def add(self, array_page):
        with open("vm.txt", mode="a") as vm1:
            vm1.write(str(array_page[0]) + " " + str(array_page[1]) + "\n")
