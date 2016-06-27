from config import Config

class LibConfig(Config):

	def __init__(self):
		Config.__init__(self, "lib.conf")

	def ipparserMapping(self):
		return self._config.get("goipparser", "mapping")

	def loggingConfigFile(self):
		if self._config.has_option("logging", "config_file"):
			return self._config.get("logging", "config_file")
		else:
			return None
