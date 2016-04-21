import json
from lib.utils import getScriptDir

class PackageManager(object):

	def __init__(self):
		self._packages = {}

	def getPackages(self, distribution = "rawhide"):
		"""
		:param distribution: package distribution
		:type  distribution: string
		:returns: [string]
		:raises KeyError: if distribution not found
		"""
		if self._packages == {}:
			file_location = "%s/data/distribution_packages.json" % getScriptDir(__file__)
			with open(file_location, "r") as f:
				packages = json.load(f)
			for pkg in packages:
				for distro in pkg["distributions"]:
					try:
						self._packages[distro].append(pkg["package"])
					except KeyError:
						self._packages[distro] = [pkg["package"]]

		return self._packages[distribution]
