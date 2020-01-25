from time import time


class Timer:
    def __init__(self):
        self.start_time = time()
        self.time_to_wait = 0
        self.waiting = False

    def start(self):
        self.start_time = time()

    def get(self):
        '''
        Get the amount of time passed since the timer began
        '''
        return time() - self.start_time

    def wait(self, time_to_wait):
        '''
        Wait for a given number of seconds
        '''
        if not self.waiting:
            self.start()
            self.time_to_wait = time_to_wait
            self.waiting = True

    def is_done(self):
        '''
        Returns whether or not the timer has finished waiting
        '''
        if self.waiting:
            if self.get() >= self.time_to_wait:
                self.waiting = False
                return True
        return False