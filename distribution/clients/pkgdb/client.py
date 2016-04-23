import requests
import logging
import json
from lib.utils import getScriptDir

from threading import Thread, enumerate
from time import sleep

__all__ = ["PkgDBClient"]

class Worker(Thread):
    def __init__(self, url, package):
        Thread.__init__(self)
        self.url = url
	self.package = package
        self.response = None

    def run(self):
	params = {"pkgname": self.package}
	self.response = requests.get(self.url, params=params)

class PkgDBClient(object):

	def __init__(self):
		self.base_url = "https://admin.fedoraproject.org/pkgdb/api"

	def packageExists(self, package):
		"""Check if the package already exists

		:param package: package name
		:type  package: string
		"""
		url = "%s/packages" % self.base_url
		params = {"pattern": package}
		response = requests.get(url, params=params)
		if response.status_code != requests.codes.ok:
			return False

		return True

	def _getPackageBranches(self, packages):
		url = "%s/package" % self.base_url
		workers = [ Worker(url, package) for package in packages ]
		for worker in workers:
			worker.start()

		while True:
			running = map(lambda l: l.isAlive(), workers)
			if not reduce(lambda a,b: a or b, running):
				break

		branches = {}
		for worker in workers:
			if worker.response.status_code != requests.codes.ok:
				logging.error("Unable to retrieve data for %s package" % worker.package)
				branches[worker.package] = []
				continue

			branches[worker.package] = map(lambda l: l["collection"]["branchname"], worker.response.json()["packages"])

		return branches

	def _processPackageData(self, data):
		return {
			"name": data["name"],
			"creation_date": data["creation_date"]
		}

	def getCollections(self):
		url = "%s/collections" % self.base_url
		response = requests.get(url)
		if response.status_code != requests.codes.ok:
			return {}

		data = response.json()
		if data["output"] != "ok":
			logging.error("Unable to get PkgDB collections")
			return {}

		collections = {}
		for collection in data["collections"]:
			if collection["status"] not in  ["Active", "Under Development"]:
				continue

			if collection["name"] not in collections:
				collections[ collection["name"] ] = {}


			if collection["koji_name"] not in collections[ collection["name"] ]:
				collections[ collection["name"] ][ collection["koji_name"] ] = {}

			collections[ collection["name"] ][ collection["koji_name"] ] = {"dist_tag": collection["dist_tag"][1:]}

		return collections

	def getGolangPackages(self):
		"""Get a list of all golang packages for all available branches
		"""

		packages = {}

		# get all packages
		url = "%s/packages" % self.base_url
		params = {"pattern": "golang-*", "limit": 200}
		response = requests.get(url, params=params)
		if response.status_code != requests.codes.ok:
			return {}

		data = response.json()
		for package in data["packages"]:
			packages[package["name"]] = self._processPackageData(package)

		# accumulate packages from all pages
		for page in range(2, data["page_total"] + 1):
			params = {"pattern": "golang-*", "limit": 200, "page": page}
			response = requests.get(url, params=params)
			if response.status_code != requests.codes.ok:
				continue

			data = response.json()
			for package in data["packages"]:
				packages[package["name"]] = self._processPackageData(package)

		# get branches of all packages
		MAX_LEN = 30
		# break the list of packages into lists of at most 50 packages
		package_names = packages.keys()
		for i in range(0, len(package_names), MAX_LEN):
			sublist = package_names[i:i+MAX_LEN]
			branches = self._getPackageBranches(sublist)
			for package in sublist:
				packages[package]["branches"] = branches[package]

		return packages


class FakePkgDBClient(object):

	def __init__(self):
		pass

	def packageExists(self, package):
		return False

	def getGolangPackages(self):
		
		with open("%s/fakedata.json" % getScriptDir(__file__), "r") as f:
			return json.load(f)
