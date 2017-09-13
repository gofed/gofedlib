try:
        import ConfigParser as configparser
except:
        import configparser


from gofedlib.utils import getScriptDir
import os

class Config(object):

	def __init__(self, config_file):
		config_etc = "/etc/gofed/%s" % config_file
		config_default = "%s/%s" % (self._classDir(), config_file)

		if os.path.isfile(config_etc):
			self._parse(config_etc)
		else:
			self._parse(config_default)

	def _classDir(self):
		return getScriptDir(__file__)

	def _parse(self, config_file):
		self._config = configparser.ConfigParser()
		self._config.read(config_file)

