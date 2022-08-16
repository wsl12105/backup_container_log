#!/usr/bin/python

# This is script use to backup docker container log
# if log size greater than 100M.
# and delete backup log 2days ago

import os
from shutil import copy
import time

basedir = "/var/lib/docker/containers/"
containersdir = os.listdir(basedir)
two_days = 86400 * 2

def get_log():
    container_logs = []
    for container in containersdir:
        container_path = os.path.join(basedir, container)
        for log in os.listdir(container_path):
            if log.endswith('json.log'):   #match log file
                container_log = os.path.join(container_path, log)
                container_logs.append(container_log)
   
    return container_logs


def back_log(logs):
    maxlogsize = 100  #container log max size M
    current_time = time.strftime("%Y%m%d_%H:%M:%S")
    logbackups = []
    for log in logs:
        log_size = os.path.getsize(log) / 1024 / 1024
        logbackup = log + "-" +current_time + "-backup"
        if log_size > maxlogsize:
            copy(log, logbackup)
            with open(log, "r+") as f:
                f.truncate()   # clear log 
     
        #logbackups.append(logbackup)    
   # return logbackups

def get_back_log():
    back_logs = []
    for container in containersdir:
        container_path = os.path.join(basedir, container)
        for log in os.listdir(container_path):
            if log.endswith('-backup'):   #match back log file
                back_log = os.path.join(container_path, log)
                back_logs.append(back_log)

    return back_logs

def remove_back_log(backuplog):
    # remove 2days old back logs
    # unix time 1 day 86400
    
    current = time.time()
    for bklog in backuplog:
        bklog_mtime = os.path.getmtime(bklog) #get back logfile last modify time 
        if current - bklog_mtime > two_days:
            os.remove(bklog)

def main():
    while True:
        back_log(get_log())
        remove_back_log(get_back_log())
        time.sleep(two_days)

if __name__ == "__main__":
    main()
