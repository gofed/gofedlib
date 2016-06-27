from lib.config.libconfig import LibConfig
import yaml
import logging
import logging.config
import os
from lib.utils import getScriptDir

class Logger(object):

	@staticmethod
	def set(verbose=False):
		if LibConfig().loggingConfigFile() is not None:
			config_file = LibConfig().loggingConfigFile()
		else:
			config_file = "%s/logging.yaml" % getScriptDir(__file__)

		log_config = yaml.load(open(config_file, 'r'))
		if verbose:
			log_config["handlers"]["consoleHandler"]["level"] = "INFO"
		logging.config.dictConfig(log_config)

