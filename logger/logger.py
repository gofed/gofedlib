from lib.config.config import Config
import yaml
import logging
import logging.config

class Logger(object):

	@staticmethod
	def set(verbose=False):
		config_file = Config().loggingConfigFile()
		log_config = yaml.load(open(Config().loggingConfigFile(), 'r'))
		if verbose:
			log_config["handlers"]["consoleHandler"]["level"] = "INFO"
		logging.config.dictConfig(log_config)

