from subprocess import PIPE, Popen
import os
import time
import datetime

def getScriptDir(file = __file__):
	return os.path.dirname(os.path.realpath(file))

def runCommand(cmd):
	process = Popen(cmd, stderr=PIPE, stdout=PIPE, shell=True)
	stdout, stderr = process.communicate()
	rt = process.returncode
	
	return stdout, stderr, rt

def dateToTimestamp(date):
	return time.mktime(datetime.datetime.strptime(date, "%Y-%m-%d").timetuple())

