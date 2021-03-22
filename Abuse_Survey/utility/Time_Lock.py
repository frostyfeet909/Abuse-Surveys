# Program to instanciate Time Lock class
from time import time, sleep


class Time_Lock:
    """
    Class to imitate threading.Lock based on a timeout
    """

    def __init__(self, timeout=2):
        """
            timeout - Required locking timout : Float
        """
        self.last_time = 0
        self.timeout = timeout

    def acquire(self):
        """
        Acquire timeout lock
        """
        time_diff = time()-self.last_time

        # Sleep untill timeout is over
        if time_diff < self.timeout:
            sleep((self.timeout-time_diff))

    def release(self):
        """
        Release timeout lock
        """
        self.last_time = time()
