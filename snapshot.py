class Snapshot(object):

	def __init__(self):
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
