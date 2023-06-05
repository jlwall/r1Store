import findR1S as fR
import time
from datetime import datetime
from PIL import Image
from selenium.webdriver.common.by import By
from selenium import webdriver
import sys
import traceback


x = 0
rivUser = "<email>"
rivPass = "<your-PW-Here>"
poKey = "<somePOKey>"
poUser = "poUser"

while x == 0:
    now = datetime.now()
    current_time = now.strftime("%Y-%b-%d_%H_%M_%S")
    print("Current Time =", current_time)
    try:
        driver = webdriver.Safari()
        x = fR.findR1S(driver,rivUser,rivPass, poKey, poUser)
    except Exception as ex:
        # Get current system exception
        ex_type, ex_value, ex_traceback = sys.exc_info()

        # Extract unformatter stack traces as tuples
        trace_back = traceback.extract_tb(ex_traceback)

        # Format stacktrace
        stack_trace = list()

        for trace in trace_back:
            stack_trace.append("File : %s , Line : %d, Func.Name : %s, Message : %s" % (trace[0], trace[1], trace[2], trace[3]))

        print("Exception type : %s " % ex_type.__name__)
        print("Exception message : %s" %ex_value)
        print("Stack trace : %s" %stack_trace)
        driver.close()
        x = 0

    if x == 1:
        print("\tSleeping For 1 hour")
        print("FOUND")
        x=0
        time.sleep(20*60) #pause for 1 hour
    else:
        print("\tSleeping For 5 minutes")
        time.sleep(5*60) #pause for 5 minutes
