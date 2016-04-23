from .upstreamprovider import UpstreamProvider
import os
import json
from lib.utils import getScriptDir

class ProviderBuilder(object):

	def buildUpstreamWithLocalMapping(self):
		mapping_file = os.path.join(getScriptDir(__file__), "data/ip2pp_mapping.json")

		with open(mapping_file, "r") as f:
			ip2pp = json.load(f)

		p = UpstreamProvider(ip2pp)

		return p
