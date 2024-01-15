"""
author @ kumar dahal
date: jun 5 2023
this is the logger of the project
"""

import os
import sys
import logging
import pandas as pd
from ASLD_step2.constants import get_current_time_stamp



LOG_DIR="logs"

"""
this function is written to create the log file ,
where we fetch the constant current time stamp function and create the file so that at each run we can create unique file
"""
def get_log_file_name():
    return f"log_{(get_current_time_stamp)}.log"

#create directory to store log files
LOG_FILE_NAME = get_log_file_name()

#check if exist or not if exist don't create it
os.makedirs(LOG_DIR,exist_ok=True)

#logs/1685974218.log
LOG_FILE_PATH = os.path.join(LOG_DIR,LOG_FILE_NAME)


#writin log format
logging.basicConfig(filename=LOG_FILE_PATH,
filemode="w",
format='[%(asctime)s]^;%(levelname)s^;%(lineno)d^;%(filename)s^;%(funcName)s()^;%(message)s',
level=logging.INFO
)

"""
this function is  is to write log in filename 
"""

def get_log_dataframe(file_path):
    data=[]
    #get the log file containing of log information
    with open(file_path) as log_file:
        #itterate over each info
        for line in log_file.readlines():
            #split based on delimeter and append into data
            data.append(line.split("^;"))
    #convert the list into dataframe
    log_df = pd.DataFrame(data)
    #create the columns for datframe
    columns=["Time stamp","Log Level","line number","file name","function name","message"]
    #add the columns to dataframe
    log_df.columns=columns
    #add extra column  message 
    log_df["log_message"] = log_df['Time stamp'].astype(str) +":$"+ log_df["message"]

    return log_df[["log_message"]]


