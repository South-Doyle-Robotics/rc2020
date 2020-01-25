from tools import Timer


class Test:
    def __init__(self, *args, **kwargs):
        '''
        Do not overload me!
        '''
        self.testStart(*args, **kwargs)
        self.TEST_TIMER = Timer()
        self.PERIODIC_DONE = False
        self.END_DONE = False

    def run(self):
        '''
        Execute the test on the robot.

        Call this method in testPeriodic or another periodic method.
        '''
        self.TEST_TIMER.wait(1)

        if self.TEST_TIMER.is_done():
            self.PERIODIC_DONE = True

        if self.END_DONE:
            pass
        elif self.PERIODIC_DONE:
            self.testEnd()
            self.END_DONE = True
        else:
            self.testPeriodic()

    def testStart(self, *args, **kwargs):
        '''
        This is called to initialize your test.
        Instantiate any data associated with your test here.

        Any arguments passed to __init__ will also be passed to this method.

        Overload me!
        '''
        pass

    def testPeriodic(self):
        '''
        This is called to update your test.
        Put any periodic code here.

        Overload me!
        '''
        pass
    
    def testEnd(self):
        '''
        This is called to destruct your test.
        Anything used to tie off loose ends after your period methods should be called here.

        Overload me!
        '''
        pass