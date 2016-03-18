import koji
import json
from utils import getScriptDir

class KojiClient(object):
	"""Class encapsulating communication with Koji.
	It uses already create python module.
	This class is meant to be replacable with another class with the same interface.
	"""

	def __init__(self):
		server = "http://koji.fedoraproject.org/kojihub/"
		self.session = koji.ClientSession(server)

	def getLatestRPMS(self, distribution, package):
		data = self.session.getLatestRPMS(distribution, package=package)

		if len(data[1]) == 0:
			raise KeyError("'%s' package not found\n" % pkg)

		build = "%s-%s-%s" % (data[1][0]["package_name"], data[1][0]["version"], data[1][0]["release"])
		rpms = []
		for rpm in data[0]:
			rpm_obj = {
				"name": "%s-%s-%s.%s.rpm" % (rpm["name"], rpm["version"], rpm["release"], rpm["arch"])
			}

			rpms.append(rpm_obj)

		return {
			"name": build,
			"rpms": rpms
		}

class FakeKojiClient(object):

	def __init__(self):
		file_location = "%s/fakedata/nodes.json" % getScriptDir(__file__)
		self.data = {}
		with open(file_location, "r") as f:
			data = json.load(f)

		for line in data:
			parts = line["name"].split("-")
			name = "-".join(parts[:-2])
			self.data[name] = line

	def getLatestRPMS(self, distribution, package):
		return self.data[package]
