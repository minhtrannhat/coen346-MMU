import threading


class MemoryManager(threading.Thread):
    def __init__(self, clock, cmd_obj, output_file, disk_page, memory):
        super(MemoryManager, self).__init__()
        self.is_finished = False

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
        self.Locking = threading.Lock()

        # initialize output file
        self.output_file = output_file

    def set_finished(self, bool1):
        self.is_finished = bool1

    def run(self):

        print("Starting Memory Manager Thread\n")
        while not self.is_finished:
            pass
        print("Exiting Memory Manager Thread\n")

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
        # For this swap to work, we should basically perform the principle of a bubble sort with the temp values
        temporary_index_value = int(self.object_memory.Index_LRU())
        temporary_memory = self.object_memory.memory[temporary_index_value]
        temporary_disk = self.page_disk.read(Id)
        # We will make use of the functions set and write that were defined in the virtual memory and in the disk classes . Those were written for that purpose precisely

        self.object_memory.set_page(temporary_index_value, temporary_disk)
        self.page_disk.Write(temporary_memory)

        with open(self.output_file, mode="a") as f:
            f.write(
                f"Clock:{self.thread_clock.timer} Memory Manager Swap: Variable {Id} with Variable {temporary_memory[temporary_index_value]}\n"
            )
        return temporary_disk[1]

    def api(self, object_command, process_number, term_time):
        self.Locking.acquire()

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
            with open(self.output_file, mode="a") as f:
                f.write(
                    f"Clock:{self.thread_clock.timer}, Process {process_number}: {com}: Variable: {Id}\n"
                )

        elif com == "Store":
            self.status = True
            self.store_function(com1, com2)
            with open(self.output_file, mode="a") as f:
                f.write(
                    f"Clock: {self.thread_clock.timer}, Process {process_number}: {com}: Variable {Id}, Value: {com2}\n"
                )
            self.status = False
        elif com == "Lookup":
            self.thread_clock.add_timer(10)
            self.look_up_function(com1)
            with open(self.output_file, mode="a") as f:
                f.write(
                    f"Clock: {self.thread_clock.timer}, Process {process_number}: {com}: Variable {Id}, Value: {self.object_memory.get_variable(Id)}\n"
                )

        self.Locking.release()
