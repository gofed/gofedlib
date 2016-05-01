import re

class ImportPathParser(object):
	"""Decide if a given import path is native (on of packages in golang stdlib).
	If not, determine import path prefix based on a list of known prefixes.
	"""

	def __init__(self, known_ipprefixes, native_packages):
		"""
		:param known_prefixes: list of know ipprefixes, regexps expected
		:type  known_prefixes: [regexp] with at least one group
		:param native_packages: list of package prefixes from golang stdlib
		:type  native_packages: [string]
		"""
		self.known_ipprefixes = known_ipprefixes
		self.native_packages = native_packages

		self._native = False
		self._prefix = ""
		self._package = ""

	def parse(self, importpath):
		"""Parse import path. Determine if the path is native or starts with known prefix.

		:param importpath:	import path to parse
		:type  importpath:	str
		:return: bool
		"""
		# reset default values
		self.native = False
		self._prefix = ""
		self._package = ""

		url = re.sub(r'http://', '', importpath)
		url = re.sub(r'https://', '', url)

		# is import path native package?
		if url.split('/')[0] in self.native_packages["packages"]:
			self.native = True
			return self

		for regex in self.known_ipprefixes:
			match = re.search(regex, url)
			if match:
				self._prefix = match.group(1)
				if match.group(3):
					self._package = match.group(3)
				return self

		raise ValueError("Import path prefix for '%s' not recognized" % importpath)

	def isNative(self):
		return self.native

	def prefix(self):
		return self._prefix

	def package(self):
		return self._package

