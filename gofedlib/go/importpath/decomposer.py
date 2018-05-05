class ImportPathsDecomposer:

	def __init__(self, ipparser):
		self.ipparser = ipparser
		self._classes = {}

	def classes(self):
		return self._classes

	def decompose(self, importpaths):
		self._classes = {}
		for path in importpaths:
			self.ipparser.parse(path)
			if self.ipparser.isNative():
				key = "Native"
			else:
				key = self.ipparser.prefix()

			if key not in self._classes:
				self._classes[key] = [path]
			else:
				self._classes[key].append(path)

		return True
