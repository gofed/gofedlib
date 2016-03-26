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
	return int(time.mktime(datetime.datetime.strptime(date, "%Y-%m-%d").timetuple()))

def intervalsOverlap(interval1, interval2):
	s1, e1 = interval1
	s2, e2 = interval2

	# (s1, e1) < (s2, e2) or (s2, e2) < (s1, e1)
	if e1 < s2 or e2 < s1:
		return False

	# in other cases intervals overlap
	return True

def intervalCovered(interval1, interval2):
	"""Is interval1 covered by interval2?
	I.e. is interval1 subset of interval2?

	"""
	s1, e1 = interval1
	s2, e2 = interval2

	if s2 <= s1 and e1 <= e2:
		return True

	return False
