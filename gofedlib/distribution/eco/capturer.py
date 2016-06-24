import logging
logger = logging.getLogger("distribution_capturer")

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

	def captureLatest(self, distributions, custom_packages, blacklist = []):
		"""Get the latest snapshot for requested distributions

		:param distributions: list of distributions, each item as {"product": ..., "version": ...}
		:type  distributions: [{}]
		:param custom_packages: list of golang packages not prefixed with golang-*
		:type  custom_packages: [string]
		"""
		self._snapshots = {}

		# get collections
		collections = self.pkgdb_client.getCollections()

		# detect all golang packages with generic name
		packages = self.pkgdb_client.getGolangPackages()

		# scan packages
		for distribution in distributions:
			logger.info("Capturing current builds for %s" % distribution)

			snapshot = DistributionSnapshot(distribution)
			product = distribution.product()
			version = distribution.version()

			if product not in collections:
				logging.error("Product '%s' not recognized" % product)

			if version not in collections[product]:
				logging.error("Version '%s' not recognized" % version)

			branch = collections[product][version]["branch"]

			scanned_packages = sorted(list(set(packages.keys() + custom_packages) - set(blacklist)))
			scanned_packages_total = len(scanned_packages)
			scanned_packages_counter = 0

			for package in scanned_packages:
				scanned_packages_counter = scanned_packages_counter + 1
				# filter out all packages not in targeted distribution
				# custom package inherits all available branches
				if package in packages:
					if branch not in packages[package]["branches"]:
						logger.warning("No %s branch found for %s" % (branch, package))
						continue

				# get a list of rpms for given package
				try:
					data = self.koji_client.getLatestRPMS(distribution.version(), package)
				except ValueError as e:
					logger.warning(str(e))
					continue
				except KeyError as e:
					logger.warning(str(e))
					continue

				logger.info("%s/%s %s: %s rpms detected" % (
					scanned_packages_counter,
					scanned_packages_total,
					package,
					len(data["rpms"])
				))
				snapshot.setRpms(package, data["name"], data["build_ts"], data["rpms"])

			snapshot_key = "%s:%s" % (distribution.product(), distribution.version())
			self._snapshots[snapshot_key] = {"snapshot": snapshot, "distribution": distribution}

		return self

	def snapshots(self):
		return self._snapshots
