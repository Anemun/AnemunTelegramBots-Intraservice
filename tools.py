import sys, datetime
import config

def debugLog(message):
    if config.debugEnabled:
        print("{0}: {1}".format(datetime.datetime.now(), message))
        sys.stdout.flush()