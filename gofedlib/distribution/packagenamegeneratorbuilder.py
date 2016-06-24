import json
import os
from .packagenamegenerator import PackageNameGenerator
from lib.utils import getScriptDir 

class PackageNameGeneratorBuilder(object):

	def buildWithLocalMapping(self):

		with open("%s/data/ip2package_mapping.json" % getScriptDir(__file__), "r") as f:
			mapping = json.load(f)

		return PackageNameGenerator(mapping)
