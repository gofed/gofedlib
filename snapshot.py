import json

class Snapshot(object):

	def __init__(self):
		self._packages = {}

	def clear(self):
		self._packages = {}
		return self

	def addPackage(self, package, commit):
		self._packages[package] = commit
		return self

	def packages(self):
		# TODO(jchaloup): introduce iterator instead
		return self._packages

	def Godeps(self):
		"""Return the snapshot in Godeps.json form
		"""
		dict = []
		for package in sorted(self._packages.keys()):
			dict.append({
				"ImportPath": str(package),
				"Rev": str(self._packages[package])
			})

		return dict

	def GLOGFILE(self):
		"""Return the snapshot in GLOGFILE form
		"""
		lines = []
		for package in sorted(self._packages.keys()):
			lines.append("%s %s" % (str(package), str(self._packages[package])))

		return "\n".join(lines)

	def readGodepsFile(self, file):
		with open(file, "r") as f:
			data = json.load(f)

		# Deps key?
		if "Deps" not in data:
			raise ValueError("Deps key missing in %s" % file)

		packages = {}
		for package in data["Deps"]:
			if "ImportPath" not in package:
				raise ValueError("ImportPath key missing in %s" % file)

			if "Rev" not in package:
				raise ValueError("Rev key missing in %s" % file)

			packages[package["ImportPath"]] = package["Rev"]

		# The file is valid Godeps.json file
		self.clear()
		self._packages = packages

		return self
