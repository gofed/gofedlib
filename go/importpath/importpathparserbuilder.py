from goimportpathparser import GoImportPathParser
import json
from utils import getScriptDir

# TODO(jchaloup):
# - introduce buildDefault() and make it configurable

class ImportPathParserBuilder(object):

	def buildWithLocalMapping(self):
		# TODO(jchaloup): read location of mappings from config file
		with open("%s/data/known_prefixes.json" % getScriptDir(__file__), "r") as f:
			regexs = json.load(f)

		with open("%s/data/native_packages.json" % % getScriptDir(__file__), "r") as f:
			native = json.load(f)


		return ImportPathParser(regexs, native)

	def buildWithRemoteMapping(self):
		raise NotImplementedError()

