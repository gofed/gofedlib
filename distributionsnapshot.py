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

import time
import json

class DistributionSnapshot(object):

	def __init__(self, distribution = "", go_version = ""):
		self.distribution = distribution
		self.go_version = ""

		# dictionary of lists
		self.rpms = {}

		self.created = int(time.time())

	def packages(self):
		"""Get a list of packages in the snapshot.
		Each package with attached list of rpms.
		"""
		return self.rpms

	def setRpms(self, package, rpms):
		"""Add/Update package rpm
		"""
		self.rpms[package] = rpms

	def clone(self):
		"""Clone (deepcopy) snapshot
		"""
		snapshot = DistributionSnapshot(self.distribution, self.go_version)
		for package in self.rpms:
			snapshot.setRpms(package, self.rpms[package])

		return snapshot

	def json(self):
		return {
			"distribution": self.distribution,
			"go_version": self.go_version,
			"timestamp": self.created,
			"packages": self.rpms
		}

	def load(self, file):
		with open(file, "r") as f:
			data = json.load(f)

		self.distribution = data["distribution"]
		self.go_version = data["go_version"]
		self.timestamp = data["timestamp"]
		self.rpms = data["packages"]

		return self

	def compare(self, snapshot):
		"""Compare two snapshots:
		- return a list of new packages in this snapshot
		- return a list of new rpms in this snapshot

		:param snapshot: distribution snapshot
		:type  snapshot: DistributionSnapshot
		"""
		packages = snapshot.packages()

		diff_snapshot = DistributionSnapshot(self.distribution, self.go_version)

		for package in list(set(self.rpms.keys()) - set(packages.keys())):
			diff_snapshot.setRpms(package, self.rpms[package])

		new_rpms = {}
		for package in list(set(self.rpms.keys()) & set(packages.keys())):
			current_rpms = map(lambda l: l["name"], self.rpms[package])
			rpms = map(lambda l: l["name"], packages[package])
			difference = list(set(current_rpms) - set(new_rpms))
			if difference != []:
				diff_snapshot.setRpms(package, difference)

		return diff_snapshot
