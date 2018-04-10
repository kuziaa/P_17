#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from collections import deque
import threading
import time
import sys
import logging
import os

logger = logging.getLogger(__name__)
logfile = "script_log.log"
span_time = 2
run_tracker = []

formatter = logging.Formatter('%(asctime)s - %(name)s : %(threadName)10s - %(levelname)s - %(message)s')
screen_handler = logging.StreamHandler(sys.stdout)
screen_handler.setLevel(logging.DEBUG)
screen_handler.setFormatter(formatter)

file_handler = logging.FileHandler(logfile)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

logger.addHandler(screen_handler)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)

start_time = time.time()


# MODIFY-START if needed
# MODIFY-END if needed

def threaded_execution(*args, **kwargs):
    # MODIFY-START
    def wrapped(fn):
        def decorated_fn(filename):
            t = threading.Thread(target=fn, args=(filename,))
            t.start()
            return
        return decorated_fn
    return wrapped
    # MODIFY-END

@threaded_execution()
def long_long_function(filename):
    logger.info("Filename to work with: {}".format(filename))
    run_tracker.append(filename)
    time.sleep(span_time)
    # MODIFY-START
    if not os.path.isfile(filename):
        logger.error('file {} not found'.format(filename))
        raise IOError('file {} not found'.format(filename))

    last_10_lines = deque([], 10)
    with open(filename, 'r') as file_object:
        for line in file_object:
            last_10_lines.append(line)

    filename_dir, filename_name = os.path.split(filename)
    filename_for_save = '{}truncated_{}'.format(filename_dir, filename_name)
    with open(filename_for_save, 'w') as file_object:
        while last_10_lines:
            file_object.write(last_10_lines.popleft())
    # MODIFY-END


if __name__ == "__main__":
    logger.info("Starting a chain of long functions")
    long_long_function("test_file_1.txt")
    long_long_function("test_file_2.txt")
    logger.info("Starting long main logic")
    time.sleep(span_time)
    ########################
    # --- Summary part --- #
    ########################
    total_time = time.time() - start_time
    logger.info("The run took '{:.3}' seconds".format(total_time))
    assert len(run_tracker)  # Do NOT remove or change, we need to ensure long_long_function ever ran
    assert total_time < (span_time + 1)  # +1 second is granted for all the threads to get allocated

    # MODIFY-START if needed
    # MODIFY-END if needed
