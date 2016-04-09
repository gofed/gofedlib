import koji
import json
from utils import getScriptDir
import time

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
			raise KeyError("No build found for '%s' package" % package)

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

	def getPackageBuilds(self, distribution, package, since = 0, to = int(time.time()) + 86400):
		koji_builds = self.session.queryHistory(package=package)["tag_listing"]

		build_id_set = set([x['build_id'] for x in koji_builds if distribution in x['tag.name']])

		builds = {}
		for build_id in build_id_set:
			build_info = self.session.getBuild(build_id)

			bdate_ts = int(build_info["completion_ts"])

			if bdate_ts < since or bdate_ts > to:
				continue

			build_rpms = self.session.listRPMs(build_id)

			build = {
				"id": build_id,
				"build_ts": bdate_ts,
				"author": build_info["owner_name"],
				"name": build_info["nvr"],
				"architectures": list(set([x['arch']for x in build_rpms])),
				"rpms": map(lambda rpm: "%s.%s.rpm" % (rpm['nvr'], rpm['arch']), build_rpms)
			}

			builds[build_info["nvr"]] = build

		return builds

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
