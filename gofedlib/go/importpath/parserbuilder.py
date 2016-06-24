from .parser import ImportPathParser
import json
from lib.utils import getScriptDir
from lib.config.libconfig import LibConfig

class ImportPathParserBuilder(object):

	def __init__(self):
		self.mapping = LibConfig().ipparserMapping()

	def buildDefault(self):
		if self.mapping == "local":
			return self.buildWithLocalMapping()
		if self.mapping == "remote":
			return self.buildWithRemoteMapping()

		raise KeyError("Mapping '%s' set in configuration file not recognized")

	def buildWithLocalMapping(self):
		# TODO(jchaloup): read location of mappings from config file
		with open("%s/data/known_prefixes.json" % getScriptDir(__file__), "r") as f:
			regexs = json.load(f)

		with open("%s/data/native_packages.json" % getScriptDir(__file__), "r") as f:
			native = json.load(f)


		return ImportPathParser(regexs, native)

	def buildWithRemoteMapping(self):
		raise NotImplementedError()

