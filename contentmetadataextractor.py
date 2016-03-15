import os
from utils import runCommand

class ContentMetadataExtractor(object):

	def __init__(self, source_code_directory, verbose = False, skip_errors = False, check_deps_directory_prefixes = True):
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
		self.check_deps_directory_prefixes = check_deps_directory_prefixes

		self.docs = []
		self.go_directories = []
		self.non_go_directories = []
		self.licenses = []
		self._deps_dirs = []

		self._nodes = {}

	def _isDoc(self, doc):
		if doc.endswith(".md"):
			return True

		return doc in ['README', 'LICENSE', 'AUTHORS', 'COPYING', 'CONTRIBUTORS', 'HACKING', 'COPYRIGHT', 'PATENTS']

	def _isLicense(self, doc):
		return doc.lower() in ['license', 'license.txt', 'copying', 'copying.txt', 'license.md']

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

	def _detectDepsDirectory(self, subdirs):
		provider_prefix_counter = 0
		for dir in subdirs:
			for prefix in ["github.com", "google.golang.org", "bitbucket.org", "golang.org", "gopkg.in", "speter.net", "k8s.io"]:
				if dir == prefix:
					provider_prefix_counter += 1
					continue

		return provider_prefix_counter
	def _isKnownDepsDirectoryPrefix(self, directory):
		for prefix in ["/Godeps/_workspace/src", "/vendor/src", "/external"]:
			if directory.endswith(prefix):
				return True

		return False

	def extract(self):

		# get a list of directory trees without any *.go file
		root_dir_len = len(self.source_code_directory)

		self._dirs_flag = {}
		dir_files = {}
		docs = []
		license = ""
		self._nodes = {}
		deps_dirs = []

		for dirName, subdirList, fileList in os.walk(self.source_code_directory):
			dir = dirName[root_dir_len:]

			if subdirList != [] and self._detectDepsDirectory(subdirList) > 0:
				deps_dirs.append(dir)

			self._nodes[dir] = subdirList
			self._dirs_flag[dir] = False

			for file in fileList:
				if file.endswith(".go"):
					self._dirs_flag[dir] = True

				# get docs
				if self._isLicense(file):
					lic_file = "%s/%s" % (dir[1:], file)
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
			if self._dirs_flag[dir]:
				dir_files[dir] = filter(lambda l: l.endswith(".go"), fileList)

		# detect known deps directory prefixes
		if self.check_deps_directory_prefixes:
			deps_dirs = filter(lambda l: self._isKnownDepsDirectoryPrefix(l), deps_dirs)

		# minimize deps directories
		deps_dirs = sorted(deps_dirs)
		min_deps_dirs = deps_dirs
		for dir in deps_dirs:
			min_deps_dirs = filter(lambda l: l == dir or not l.startswith(dir), min_deps_dirs)
		self._deps_dirs = min_deps_dirs

		# get go directories
		self.go_directories = []
		for dir in self._dirs_flag:
			if not self._dirs_flag[dir]:
				continue

			skip = False
			for prefix in min_deps_dirs:
				if dir.startswith(prefix):
					skip = True
					break

			if skip:
				continue

			self.go_directories.append({
				"dir": dir,
				"files": dir_files[dir]
			})

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


	def getDepsDirectories(self):
		return self._deps_dirs

	def getGoDirectories(self):
		return self.go_directories

	def getProjectContentMetadata(self):
		return {
			"metadata": {
				"licenses": self.licenses,
				"docs": self.docs,
				"dependency_directories": self._deps_dirs,
				"non_go_directories": self.non_go_directories
			}
		}
