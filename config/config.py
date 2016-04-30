import ConfigParser
from gofed_lib.utils import getScriptDir
import os

class Config(object):

	def __init__(self):
		if "GOFED_DEVEL" not in os.environ:
			self.config_file = "/etc/gofed/lib.conf"
		else:
			self.config_file = "%s/lib.conf" % getScriptDir(__file__)

		self._parse(self.config_file)

	def _parse(self, config_file):
		self.config = ConfigParser.ConfigParser()
		self.config.read(config_file)

	def ipparserMapping(self):
		return self.config.get("goipparser", "mapping")

	def loggingConfigFile(self):
		return self.config.get("logging", "config_file")
