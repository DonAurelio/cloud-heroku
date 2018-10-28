import time
import os


WORKER_TIME_FILE_PATH = os.environ.get('WORKER_TIME_FILE_PATH','.')


def timer(func):
    """
        Measures the execution time of the decorated 
        function and place the resuts in a .log file
    """
    def wrapper(*args):
        start = time.perf_counter()
        code, out, err = func(*args)
        end = time.perf_counter()

        #  Save the time in miliseconds, the video processing
        #  status code, input and output files path.
        
        with lock:
            with open(WORKER_TIME_FILE_PATH,'a+') as file:
                file.write(text)


        return code, out, err

    return wrapper