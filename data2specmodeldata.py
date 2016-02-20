from importpathparserbuilder import ImportPathParserBuilder
from types import UnsupportedImportPathError

class Data2SpecModelData(object):
	"""Combine various data to provide data for spec model.
	Data in question:
		- golang-project-packages artefact

	"""

	def __init__(self):
		self.metadata = []
		self.packages = []
		self.tests = []
		self.mains = []
		self.docs = []
		self.skipped_directories = []

		self.ipparser = ImportPathParserBuilder().buildWithLocalMapping()

	def filterOutNative(self, deps):
		o_deps = []
		for dep in deps:
			try:
				if self.ipparser.parse(dep).isNative():
					continue
			except UnsupportedImportPathError:
				continue

			o_deps.append(dep)
		return o_deps

	def combine(self, metadata, project_packages, content_metadata):
		# metadata
		self.metadata = metadata

		# get packages
		self.packages = []
		for package in  project_packages["data"]["dependencies"]:
			obj = {
				"package": package["package"],
				"dependencies": self.filterOutNative(map(lambda l: l["name"], package["dependencies"]))
			}
			self.packages.append(obj)

		# get tests
		self.tests = []
		for test in project_packages["data"]["tests"]:
			obj = {
				"test": test["test"],
				"dependencies": self.filterOutNative(test["dependencies"])
			}
			self.tests.append(obj)

		# get mains
		self.mains = []
		for main in project_packages["data"]["main"]:
			obj = {
				"path": main["filename"],
				"dependencies": self.filterOutNative(main["dependencies"])
			}
			self.mains.append(obj)

		# get docs
		self.docs = content_metadata["metadata"]["docs"]

		# get license
		self.licenses = content_metadata["metadata"]["licenses"]

		# get skipped_directories
		self.skipped_directories = content_metadata["metadata"]["non_go_directories"]

	def getData(self):
		return {
			"metadata": self.metadata,
			"data": {
				"packages": self.packages,
				"tests": self.tests,
				"mains": self.mains,
				"docs": self.docs,
				"licenses": self.licenses,
				"skipped_directories": self.skipped_directories
			}
		}
