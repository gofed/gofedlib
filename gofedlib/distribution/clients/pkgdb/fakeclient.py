from client import PkgDBClient
from lib.utils import getScriptDir
import json

class FakePkgDBClient(PkgDBClient):

	def __init__(self):
		fakedata = "%s/../fakedata/data.json" % getScriptDir(__file__)
		with open(fakedata, "r") as f:
			self._data = json.load(f)

	def packageExists(self, package):
		return False

	def getGolangPackages(self):
		packages = {}
		for build in self._data["builds"]:
			packages[ build["name"] ] = {
				"branches": ["master"],
				"name": build["name"],
				"creation_date": 0
			}

		return packages

	def getCollections(self):
		return {
			"Fedora": {
				"rawhide": {
					"dist_tag": "fc25",
					"branch": "master"
				}
			}
		}

