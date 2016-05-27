from subprocess import PIPE, Popen
import os
import time
import datetime
import jinja2

RED = '\033[91m'
GREEN = '\033[92m'
BLUE = '\033[94m'
CYAN = '\033[96m'
WHITE = '\033[97m'
YELLOW = '\033[93m'
MAGENTA = '\033[95m'
GREY = '\033[90m'
BLACK = '\033[90m'
DEFAULT = '\033[99m'
ENDC = '\033[0m'

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

def renderTemplate(searchpath, template_file, template_vars):

	templateLoader = jinja2.FileSystemLoader( searchpath=searchpath )
	templateEnv = jinja2.Environment( loader=templateLoader )
	template = templateEnv.get_template( template_file )
	content = template.render( template_vars )

	return content

