class ImportPathsDecomposer:

	def __init__(self, ipparser):
		self.ipparser = ipparser

		self.classes = {}

	def getClasses(self):
		return self.classes

	def decompose(self, importpaths):
		for path in importpaths:
			try:
				self.ipparser.parse(path)
			except ValueError as e:
				logging.error(e)
				key = "Unknown"
			else:
				if self.ipparser.isNative():
					key = "Native"
				else:
					key = self.ipparser.getPrefix()

			if key not in self.classes:
				self.classes[key] = [path]
			else:
				self.classes[key].append(path)

		return True
