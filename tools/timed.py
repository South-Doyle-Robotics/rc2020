from threading import Timer


class Timed:
    '''
    A superclass used to implement delayed actions
    '''

    def __init__(self, *args, **kwargs):
        self.TIMED_TIMER = None

    def do(self, method, seconds, *args, **kwargs):
        '''
        Perform a method with a delay

        do(self, method: fn(self, *args, **kwargs), seconds: float, *args, **kwargs)

        :param method: The method to call with a delay
        :param second: The seconds to wait before calling the function
        :args: The positional arguments to supply to the function
        :kwargs: The keyword arguments to supply to the function
        '''
        self.TIMED_TIMER = Timer(seconds, method, *args, **kwargs)
        self.TIMED_TIMER.start()

    def stop(self):
        '''
        Cancel the current timed action

        stop(self)
        '''
        self.TIMED_TIMER.cancel()
