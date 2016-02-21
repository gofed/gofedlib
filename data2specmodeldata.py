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

	def _trimGodepsImports(self, godeps_import_path, deps):
		godeps_import_path_len = len(godeps_import_path)
		m_deps = []
		for dep in deps:
			if dep.startswith(godeps_import_path):
				m_deps.append(dep[godeps_import_path_len:])
				continue
			m_deps.append(dep)
		return m_deps

	def combine(self, metadata, project_packages, content_metadata):
		# metadata
		self.metadata = metadata

		godeps_import_path = "%s/Godeps/_workspace/src/" % metadata["import_path"]
		godeps_import_path_len = len(godeps_import_path)

		# get packages
		self.packages = []
		for package in  project_packages["data"]["dependencies"]:
			deps = self._filterOutNative(map(lambda l: l["name"], package["dependencies"]))
			# if Godeps is on, filter all import_path_prefix/Godeps imports
			if content_metadata["metadata"]["godeps"]:
				deps = self._trimGodepsImports(godeps_import_path, deps)

			obj = {
				"package": package["package"],
				"dependencies": deps
			}
			self.packages.append(obj)

		# get tests
		self.tests = []
		for test in project_packages["data"]["tests"]:
			deps = self._filterOutNative(test["dependencies"])
			# if Godeps is on, filter all import_path_prefix/Godeps imports
			if content_metadata["metadata"]["godeps"]:
				deps = self._trimGodepsImports(godeps_import_path, deps)
			obj = {
				"test": test["test"],
				"dependencies": deps
			}
			self.tests.append(obj)

		# get mains
		self.mains = []
		for main in project_packages["data"]["main"]:
			deps = self._filterOutNative(main["dependencies"])
			# if Godeps is on, filter all import_path_prefix/Godeps imports
			if content_metadata["metadata"]["godeps"]:
				deps = self._trimGodepsImports(godeps_import_path, deps)

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
