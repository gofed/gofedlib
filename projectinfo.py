class ProjectInfo:

	def __init__(self, ipparser):
		# TODO(jchaloup): add 'nogodeps' a.k.a. skipped_directories into new artefact
		#	Like create new extractor aimed at docs and detecting folders without source code
		self.ipparser = ipparser

		self.imported_packages = []
		self.imported_native_packages = []
		self.provided_packages = []
		self.occurrences = {}
		self.main_occurrences = {}
		self.main_packages = []
		self.test_directories = []

		self.docs = []
		self.godeps_on = False

	def getImportedPackages(self):
		return self.imported_packages

	def getImportedNativePackages(self):
		return self.imported_native_packages

	def getProvidedPackages(self):
		return self.provided_packages

	def getImportsOccurrence(self):
		return self.occurrences

	def getTestDirectories(self):
		return self.test_directories

	def getMainPackages(self):
		return self.main_packages

	def getMainOccurrence(self):
		return self.main_occurrences

	def godepsDirectoryExists(self):
		return self.godeps_on

	def construct(self, data):
		"""Construct info about a project from artefact

		:param data:	golang-project-packages artefact
		:type  data:	json/dict
		"""
		occurrences = {}
		main_occurrences = {}

		# occurrences of devel packages
		for pkg in data["data"]["dependencies"]:
			package = pkg["package"]
			for item in pkg["dependencies"]:
				dep = item["name"]
				if package != ".":
					deps = map(lambda l: "%s/%s" % (package, l), item["location"])
				else:
					deps = item["location"]
				if dep not in occurrences:
					occurrences[dep] = deps
				else:
					occurrences[dep] = occurrences[dep] + deps

		self.occurrences = occurrences

		# occurrences of main packages
		for main in data["data"]["main"]:
			filename = main["filename"]
			for dep in main["dependencies"]:
				if dep not in main_occurrences:
					main_occurrences[dep] = [filename]
				else:
					main_occurrences[dep].append(filename)

		self.main_occurrences = main_occurrences
	
		# test directories
		self.test_directories = sorted(map(lambda l: l["test"], data["data"]["tests"]))

		# provided devel packages
		self.provided_packages = sorted(data["data"]["packages"])

		# imported paths in devel packages
		imported_packages = []
		imported_native_packages = []
		for path in occurrences:
			self.ipparser.parse(path)
			if self.ipparser.isNative():
				imported_native_packages.append(path)
			else:
				imported_packages.append(path)

		self.imported_packages = sorted(imported_packages)
		self.imported_native_packages = sorted(imported_native_packages)

		# main packages
		self.main_packages = map(lambda l: l["filename"], data["data"]["main"])
