import ConfigParser

class Config(object):

	def __init__(self):
		self.config_file = "/home/jchaloup/Projects/gofed/infra/third_party/gofed_lib/config/lib.conf"
		self._parse(self.config_file)

	def _parse(self, config_file):
		self.config = ConfigParser.ConfigParser()
		self.config.read(config_file)

	def ipparserMapping(self):
		return self.config.get("goipparser", "mapping")

