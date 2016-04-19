#
# Convert various formats of distribution names to unique
# distribution signature
# E.g. "Fedora 23"  => {"product": "Fedora", "version": "23"}
#      "F22"        => {"product": "Fedora", "version": "22"}
#      "Fedora:f22" => {"product": "Fedora", "version": "22"}
#
# Fedora:rawhide or any variations are not supported as rawhide is relative and changes over time

import re

class DistributionNameParser(object):

	def __init__(self):
		self.product = ""
		self.version = ""

	def _parseFedora(self, name):
		for regex in [r"Fedora\s*(\d\d?)", r"F(\d\d?)", r"Fedora:f?(\d\d?)"]:
			groups = re.search(regex, name)
			if groups:
				return groups
		return None

	def parse(self, name):
		"""Parse distribution string

		:param name: distribution string, e.g. "Fedora 23"
		:type  name: string
		"""
		name = name.strip()
		groups = self._parseFedora(name)
		if groups:
			self.product = "Fedora"
			self.version = groups.group(1)
			return self

		raise ValueError("Distribution name '%s' not recognized" % name)

	def getSignature(self):
		"""Get distribution signature

		:returns: dictionary with product and version
		:type: dict
		"""
		return {
			"product": self.product,
			"version": self.version
		}

