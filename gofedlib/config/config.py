import ConfigParser
from gofedlib.utils import getScriptDir
import os

class Config(object):

	def __init__(self, config_file):
		if "GOFED_DEVEL" not in os.environ:
			config_file_path = "/etc/gofed/%s" % config_file
		else:
			config_file_path = "%s/%s" % (self._classDir(), config_file)

		self._parse(config_file_path)

	def _classDir(self):
		return getScriptDir(__file__)

	def _parse(self, config_file):
		self._config = ConfigParser.ConfigParser()
		self._config.read(config_file)

