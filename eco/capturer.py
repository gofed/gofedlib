import logging
from ..distributionsnapshot import DistributionSnapshot

class EcoCapturer(object):
	"""Capture state of golang projects in given distributions

	"""

	def __init__(self, koji_client, pkgdb_client):
		"""Set the capturer with koji and pkgdb clients

		:param koji_client: Koji client
		:type  koji_client: KojiClient or FakeKojiClient
		:param pkgdb_client: PkgDB client
		:type  pkgdb_client: PkgDBClient or FakePkgDBClient
		"""
		self.koji_client = koji_client
		self.pkgdb_client = pkgdb_client
		self._snapshots = {}

	def captureLatest(self, distributions, custom_packages):
		"""Get the latest snapshot for requested distributions

		:param distributions: list of distributions, each item as {"product": ..., "version": ...}
		:type  distributions: [{}]
		:param custom_packages: list of golang packages not prefixed with golang-*
		:type  custom_packages: [string]
		"""
		self._snapshots = {}

		# detect all golang packages with generic name
		packages = self.pkgdb_client.getGolangPackages()

		# scan packages
		for distribution in distributions:
			logging.info("Scanning %s:%s..." % (distribution["product"], distribution["version"]))
			snapshot = DistributionSnapshot(distribution)

			for package in packages.keys() + custom_packages:
				# filter out all packages not in targeted distribution
				# custom package inherits all available branches
				if package in packages:
					if distribution["version"] == "rawhide":
						branch = "master"
					else:
						branch = distribution["version"]
	
					if branch not in packages[package]["branches"]:
						continue

				# get a list of rpms for given package
				try:
					data = self.koji_client.getLatestRPMS(distribution["version"], package)
				except ValueError as e:
					logging.error(e)
					continue
				except KeyError as e:
					logging.error(e)
					continue

				snapshot.setRpms(package, data["name"], data["rpms"])

			snapshot_key = "%s:%s" % (distribution["product"], distribution["version"])
			self._snapshots[snapshot_key] = {"snapshot": snapshot, "distribution": distribution}

		return self

	def snapshots(self):
		return self._snapshots
