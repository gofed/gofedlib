#
# Distribution Snapshot
#
# Capture a state (to a given date) of golang rpms in a given distribution.
# It is build on the same principle as Project Snapshot.
# Basic building elements corresponds to distribution packages.
# Each package provides on or more rpms (devel, unit-test, main).
# Packages with no build are not captured.
# 
# Distribution snapshot covers only packages and its rpms.
# It is not meant to capture dependencies between rpms.
#
# TODO(jchaloup):
# - snapshot manager extended by distribution snapshot manager
# - integrate orphaned packages as well (maybe not needed as the latest rpm gets fixed), what koji client returns for orphaned package?
# - introduce snapshot interpreter (to distinguish devel, unit-test and other rpm types) and snapshot filter (to return only rpms with specified label)

import time
import json

class DistributionSnapshot(object):

	def __init__(self, distribution = "", go_version = ""):
		self._distribution = distribution
		self.go_version = ""

		# dictionary of lists
		self._builds = {}

		self.created = int(time.time())

	def builds(self):
		"""Get a list of packages in the snapshot.
		Each package with attached list of rpms.
		"""
		return self._builds

	def distribution(self):
		return self._distribution

	def setRpms(self, package, build, build_ts, rpms):
		"""Add/Update package rpm
		"""
		self._builds[package] = {"build": build, "build_ts": build_ts, "rpms": rpms}
		print {"build": build, "build_ts": build_ts, "rpms": rpms}

	def clone(self):
		"""Clone (deepcopy) snapshot
		"""
		snapshot = DistributionSnapshot(self.distribution(), self.go_version)
		for package in self.builds:
			snapshot.setRpms(package, self.builds[package]["build"], self.builds[package]["build_ts"], self.builds[package]["rpms"])

		return snapshot

	def json(self):
		builds = []
		for package in self._builds:
			builds.append({
				"name": package,
				"build": self._builds[package]["build"],
				"build_ts": self._builds[package]["build_ts"],
				"rpms": map(lambda l: l["name"], self._builds[package]["rpms"])
			})

		return {
			"distribution": self.distribution(),
			"go_version": self.go_version,
			"timestamp": self.created,
			"builds": builds
		}

	def read(self, data):
		self._distribution = data["distribution"]
		self.go_version = data["go_version"]
		self.timestamp = data["timestamp"]

		builds = {}
		for build in data["builds"]:
			builds[build["name"]] = {"build": build["build"], "build_ts": build["build_ts"], "rpms": build["rpms"]}

		self._builds = builds

		return self

	def load(self, file):
		with open(file, "r") as f:
			data = json.load(f)

		self._distribution = data["distribution"]
		self.go_version = data["go_version"]
		self.timestamp = data["timestamp"]
		self._builds = data["builds"]

		return self

	def compare(self, snapshot):
		"""Compare two snapshots:
		- return a list of new packages in this snapshot
		- return a list of new builds in this snapshot

		:param snapshot: distribution snapshot
		:type  snapshot: DistributionSnapshot
		"""
		builds = snapshot.builds()

		diff_snapshot = DistributionSnapshot(self.distribution(), self.go_version)

		for package in list(set(self._builds.keys()) - set(builds.keys())):
			diff_snapshot.setRpms(package, self._builds[package]["build"], self._builds[package]["build_ts"], self._builds[package]["rpms"])

		for package in list(set(self._builds.keys()) & set(builds.keys())):
			if self._builds[package]["build"] != builds[package]["build"]:
				diff_snapshot.setRpms(package, self._builds[package]["build"], self._builds[package]["build_ts"], self._builds[package]["rpms"])

		# Assuming no package get ever removed (even if retired)
		return diff_snapshot
