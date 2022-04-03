from collections import defaultdict


class Main_Memory:
    def __init__(self, number_of_pages):
        self.memory = []
        self.number_of_pages = number_of_pages
        self.access_memory_value = defaultdict(lambda: 0)
        self.increment = 0

    def full(self):
        return len(self.memory) == self.number_of_pages
        # if the len of my memory  is bigger than my number of pages, this function will return TRUE

    def add_to_main_memory(self, Id, Value):
        for i in range(len(self.memory)):
            if str(self.memory[i][0]) == str(Id):
                self.memory[i][1] = str(Value)
                self.increment += 1
                self.access_memory_value[Id] = self.increment
                return

        if not self.full():
            self.memory.append([str(Id), str(Value)])
            self.increment += 1
            self.access_memory_value[Id] = self.increment

    def get_variable(self, Id):
        for mem in self.memory:
            if mem[0] == str(Id):
                self.increment += 1
                self.access_memory_value[Id] = self.increment
                return mem[1]
        return -1

    def Index_LRU(self):
        a = self.access_memory_value.items()
        if len(a) == 0:
            return self.memory[0][0]
        return int(min(a, key=lambda v: v[1])[0]) - 1

    def release(self, Id):
        for mem in self.memory:
            if mem[0] == str(Id):
                self.memory.remove(mem)
                self.increment += 1
                self.access_memory_value[Id] = self.increment
                return

    def set_page(self, index, page):
        page = page.strip().split()
        s = list(page)
        print(s)
        self.memory[index] = s
        self.increment += 1
        self.access_memory_value[index] = self.increment
