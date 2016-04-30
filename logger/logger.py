from lib.config.config import Config
import yaml
import logging
import logging.config
import os
from lib.utils import getScriptDir

class Logger(object):

	@staticmethod
	def set(verbose=False):
		if "GOFED_DEVEL" in os.environ:
			config_file = "%s/logging.yaml" % getScriptDir(__file__)
		else:
			config_file = Config().loggingConfigFile()

		log_config = yaml.load(open(config_file, 'r'))
		if verbose:
			log_config["handlers"]["consoleHandler"]["level"] = "INFO"
		logging.config.dictConfig(log_config)

