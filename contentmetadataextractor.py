import os
from utils import runCommand

class ContentMetadataExtractor(object):

	def __init__(self, source_code_directory, verbose = False, skip_errors = False):
		"""
		:param source_code_directory:	source code directory
		:type  source_code_directory:	str
		:param verbose:			verbose mode
		:type  verbose:			bool
		:param skip_errors:		error skipping
		:type  skip_errors:		bool
		"""
		self.source_code_directory = source_code_directory

		"""Setting implicit flags"""
		self.verbose = verbose
		self.skip_errors = skip_errors

		self.docs = []
		self.non_go_directories = []
		self.licenses = []

		self._nodes = {}

	def _isDoc(self, doc):
		if doc.endswith(".md"):
			return True

		return doc in ['README', 'LICENSE', 'AUTHORS', 'COPYING', 'CONTRIBUTORS', 'HACKING', 'COPYRIGHT', 'PATENTS']

	def _isLicense(self, doc):
		return doc.lower() in ['license', 'license.txt', 'copying', 'copying.txt']

	def _getLicense(self, doc):
		so, se, rc = runCommand("licensecheck %s" % doc)
		if rc == 0:
			return ":".join(so.split("\n")[0].split(":")[1:]).strip()
		return "Unknown"

	def _orNodes(self, node = ""):
		_or  = False

		if self._nodes[node] == []:
			return self._dirs_flag[node]

		for n in self._nodes[node]:
			_or = _or or self._orNodes("%s/%s" % (node, n))

		self._dirs_flag[node] = _or

		return _or		

	def extract(self):

		# get a list of directory trees without any *.go file
		root_dir_len = len(self.source_code_directory)

		self._dirs_flag = {}
		docs = []
		license = ""
		self._nodes = {}

		for dirName, subdirList, fileList in os.walk(self.source_code_directory):
			dir = dirName[root_dir_len:]

			self._nodes[dir] = subdirList
			self._dirs_flag[dir] = False

			for file in fileList:
				if file.endswith(".go"):
					self._dirs_flag[dir] = True

				# get docs
				if self._isLicense(file):
					lic_file = "%s/%s" % (dirName[root_dir_len+1:], file)
					if lic_file[0] == "/":
						lic_file = lic_file[1:]

					obj = {
						"file": lic_file,
						"type": self._getLicense("%s/%s" % (dirName, file))
					}
					self.licenses.append(obj)
					continue

				if self._isDoc(file):
					docs.append("%s/%s" % (dir, file))

		# get non-go directories
		non_go_directories = []

		self._orNodes()
		nodes = [""]
		while nodes != []:
			parent = nodes[-1]
			for children in self._nodes[parent]:
				node = "%s/%s" % (parent, children)
				if self._dirs_flag[node] == 0:
					non_go_directories.append(node)
				else:
					nodes.insert(0, node)
			nodes.pop()

		self.docs = map(lambda l: l[1:], docs)
		self.non_go_directories = map(lambda l: l[1:], non_go_directories)

	def getProjectContentMetadata(self):
		return {
			"metadata": {
				"licenses": self.licenses,
				"docs": self.docs,
				"deps_directories": [],
				"non_go_directories": self.non_go_directories
			}
		}
