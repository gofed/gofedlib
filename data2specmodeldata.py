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
		self.dependency_directories = []

		self.ipparser = ImportPathParserBuilder().buildWithLocalMapping()

	def _filterOutNative(self, deps):
		o_deps = []
		for dep in deps:
			try:
				if self.ipparser.parse(dep).isNative():
					continue
			except UnsupportedImportPathError:
				continue

			o_deps.append(dep)
		return o_deps

	def _trimDependencyDirectoryPrefixes(self, prefixes, deps):
		m_deps = deps
		for prefix in prefixes:
			prefix_len = len(prefix)
			m_deps = map(lambda l: l[prefix_len:] if l.startswith(prefix) else l, m_deps)
		return m_deps

	def combine(self, metadata, project_packages, content_metadata):
		# metadata
		self.metadata = metadata

		dependency_directories = map(lambda l: "%s%s/" % (metadata["import_path"], l), content_metadata["metadata"]["dependency_directories"])

		# get packages
		self.packages = []
		for package in  project_packages["data"]["dependencies"]:
			deps = self._filterOutNative(map(lambda l: l["name"], package["dependencies"]))
			# if dependency directory is on, filter out all imports prefixed with known dependency directory prefix
			if deps != [] and dependency_directories != []:
				deps = self._trimDependencyDirectoryPrefixes(dependency_directories, deps)

			obj = {
				"package": package["package"],
				"dependencies": deps
			}
			self.packages.append(obj)

		# get tests
		self.tests = []
		for test in project_packages["data"]["tests"]:
			deps = self._filterOutNative(test["dependencies"])
			# if dependency directory is on, filter out all imports prefixed with known dependency directory prefix
			if deps != [] and dependency_directories != []:
				deps = self._trimDependencyDirectoryPrefixes(dependency_directories, deps)

			obj = {
				"test": test["test"],
				"dependencies": deps
			}
			self.tests.append(obj)

		# get mains
		self.mains = []
		for main in project_packages["data"]["main"]:
			deps = self._filterOutNative(main["dependencies"])
			# if dependency directory is on, filter out all imports prefixed with known dependency directory prefix
			if deps != [] and dependency_directories != []:
				deps = self._trimDependencyDirectoryPrefixes(dependency_directories, deps)

			obj = {
				"path": main["filename"],
				"dependencies": deps
			}
			self.mains.append(obj)

		# get docs
		self.docs = content_metadata["metadata"]["docs"]

		# get license
		self.licenses = content_metadata["metadata"]["licenses"]

		# get skipped_directories
		self.skipped_directories = content_metadata["metadata"]["non_go_directories"]

		# get dependency directories
		self.dependency_directories = map(lambda l: l[1:] if l[0] == "/" else l, content_metadata["metadata"]["dependency_directories"])

	def getData(self):
		return {
			"metadata": self.metadata,
			"data": {
				"packages": self.packages,
				"tests": self.tests,
				"mains": self.mains,
				"docs": self.docs,
				"licenses": self.licenses,
				"skipped_directories": self.skipped_directories,
				"dependency_directories": self.dependency_directories
			}
		}
