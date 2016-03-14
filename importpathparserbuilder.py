from importpathparser import ImportPathParser
import json
from utils import getScriptDir

class ImportPathParserBuilder(object):

	def buildWithLocalMapping(self):
		# TODO(jchaloup): read location of mappings from config file
		ip2pp_location = "%s/data/import_path_to_provider_prefix_mapping.json" % getScriptDir(__file__)
		ip2pkg_location = "%s/data/import_path_to_package_name_mapping.json" % getScriptDir(__file__)
		native_packages_location = "%s/data/native_packages.json" % getScriptDir(__file__)

		# get mappings
		with open(ip2pp_location, "r") as f:
			ip2pp_mapping = json.load(f)

		with open(ip2pkg_location, "r") as f:
			ip2pkg_mapping = json.load(f)

		with open(native_packages_location, "r") as f:
			native_packages = json.load(f)

		return ImportPathParser(ip2pp_mapping, ip2pkg_mapping, native_packages["packages"])

	def buildWithRemoteMapping(self):
		# TODO(jchaloup): read location of mappings from config file
		# TODO(jchaloup): change path to remote mappings to point to server
		ip2pp_location = "%s/data/import_path_to_provider_prefix_mapping.json" % getScriptDir(__file__)
		ip2pkg_location = "%s/data/import_path_to_package_name_mapping.json" % getScriptDir(__file__)

		raise NotImplementedError()

	def buildWithLocalMappingForIPPrefixDecomposer(self):
		# TODO(jchaloup): read location of mappings from config file
		ip2pp_location = "%s/data/import_path_to_provider_prefix_mapping.json" % getScriptDir(__file__)

		# get mappings
		with open(ip2pp_location, "r") as f:
			ip2pp_mapping = json.load(f)

		return ImportPathParser(ip2pp_mapping, {}, [])
