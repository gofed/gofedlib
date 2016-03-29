class Snapshot(object):

	def __init__(self):
		self.packages = {}

	def clear(self):
		self.packages = {}

	def addPackage(self, package, commit):
		self.packages[package] = commit

	def Godeps(self):
		"""Return the snapshot in Godeps.json form
		"""
		dict = []
		for package in sorted(self.packages.keys()):
			dict.append({
				"ImportPath": str(package),
				"Rev": str(self.packages[package])
			})

		return dict

	def GLOGFILE(self):
		"""Return the snapshot in GLOGFILE form
		"""
		lines = []
		for package in sorted(self.packages.keys()):
			lines.append("%s %s" % (str(package), str(self.packages[package])))

		return "\n".join(lines)
