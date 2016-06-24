#
# Convert various formats of distribution names to unique
# distribution signature
# E.g. "Fedora 23"  => {"product": "Fedora", "version": "23"}
#      "F22"        => {"product": "Fedora", "version": "22"}
#      "Fedora:f22" => {"product": "Fedora", "version": "22"}
#
# Fedora:rawhide or any variations are not supported as rawhide is relative and changes over time

import re

class DistributionNameSignature(object):

	def __init__(self, product, version):
		self._product = product
		self._version = version

	def product(self):
		return self._product

	def version(self):
		return self._version

	def __repr__(self):
		return "%s %s" % (self._product, self._version)

	def json(self):
		return {
			"product": self._product,
			"version": self._version
		}

	def load(self, data):
		self._product = data["product"]
		self._version = data["version"]

class DistributionNameParser(object):

	def __init__(self):
		self._signature = None

	def _parseFedora(self, name):
		for regex in [r"Fedora\s*(\d\d?)", r"F(\d\d?)", r"Fedora:f?(\d\d?)", r"Fedora:(rawhide)"]:
			groups = re.search(regex, name)
			if groups:
				return groups
		return None

	def signature(self):
		return self._signature

	def parse(self, name):
		"""Parse distribution string

		:param name: distribution string, e.g. "Fedora 23"
		:type  name: string
		"""
		name = name.strip()
		groups = self._parseFedora(name)
		if groups:
			self._signature = DistributionNameSignature("Fedora", groups.group(1))
			return self

		raise ValueError("Distribution name '%s' not recognized" % name)

