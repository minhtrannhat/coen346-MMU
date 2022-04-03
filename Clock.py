import time
import threading


class clock(threading.Thread):
    def __init__(self):
        super(clock, self).__init__()
        # is finished will be used by all classes that uses thread in order to terminate them at the end
        self.is_finished = False
        self.timer = 0  # timer counts time that passes

    def set_finished(self, bool1):  # this set terminate is needed to end the threads
        self.is_finished = bool1

    def add_timer(self, elapsed):
        self.timer += elapsed
        new_elapsed = elapsed / 1000
        time.sleep(new_elapsed)

    def run(self):
        print("Start Clock thread ")

        while not self.is_finished:
            time.sleep(1 / 10)
            self.timer = self.timer + 100

        print("\nClock thread finished\n")
        print("Exit Clock thread")
