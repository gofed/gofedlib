from client import KojiClient
import json
from lib.utils import getScriptDir

class FakeKojiClient(object):

	def __init__(self):
		file_location = "%s/../fakedata/data.json" % getScriptDir(__file__)
		self._data = {}
		with open(file_location, "r") as f:
			data = json.load(f)

		for build in data["builds"]:
			self._data[ build["name"] ] = build

	def getLatestRPMS(self, distribution, package):
		build = self._data[package]
		return {
			"name": build["build"],
			"build_ts": build["build_ts"],
			"rpms": map(lambda l: {"name": l}, build["rpms"])
		}

	def getPackageBuilds(self, distribution, package, since = 0, to = 0):
		return {
			"gofed-0.0.10-3.fc24": {
				"id": 1,
				"build_ts": 1,
				"author": "author",
				"name": "gofed-0.0.10-3.fc24",
				"architectures": ["x86_64", "ppc64le"],
				"rpms": [
					"gofed-0.0.10-3.fc24.src.rpm",
					"gofed-0.0.10-3.fc24.x86_64.rpm",
					"gofed-build-0.0.10-3.fc24.noarch.rpm"
				]
			},
			"gofed-0.0.10-2.fc24": {
				"id": 1,
				"build_ts": 1,
				"author": "author",
				"name": "gofed-0.0.10-2.fc24",
				"architectures": ["x86_64", "ppc64le"],
				"rpms": [
					"gofed-0.0.10-2.fc24.src.rpm",
					"gofed-0.0.10-2.fc24.x86_64.rpm",
					"gofed-build-0.0.10-2.fc24.noarch.rpm"
				]
			}
		}

