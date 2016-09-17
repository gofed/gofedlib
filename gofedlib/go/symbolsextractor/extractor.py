import os
import logging
import json
from lib.utils import getScriptDir, runCommand
from .coder import GoTypeCoder
from ..contentmetadataextractor import ContentMetadataExtractor
from lib.types import ExtractionError

class GoSymbolsExtractor(object):
	"""
	Input:
	 - directory to parse
	 - directories to skip
	Output:
	 - exported API
	 - imported packages
	 - occurence of imported packages
	 - test directories
	 - main packages
	 - is Godeps directory present (an others)?
	Configuration:
	 - verbose mode
	 - log directory
	 To make the class config indepenent, all flags
	 are passed via class methods.
	"""
	def __init__(self, source_code_directory, verbose = False, skip_errors = False):
		"""Neco
		:param source_code_directory:	source code directory
		:type  source_code_directory:	str
		:param verbose:			verbose mode
		:type  verbose:			bool
		:param skip_errors:		error skipping
		:type  skip_errors:		bool
		"""

		"""Setting implicit flags"""
		self.verbose = verbose
		self.skip_errors = skip_errors
		self.imports_only = False

		"""set implicit output"""
		self.symbols = {}
                self.symbols_position = {}
                # list of packages imported for each project's package
                self.package_imports = {}
                # list of packages imported in entire project
                self.imported_packages = []
                # occurences of imported paths in packages
                self.package_imports_occurence = {}
                self.test_directories = []
                self.test_directory_dependencies = {}
                # main packages
                self.main_packages = []
                # main packages dependencies
                self.main_package_deps = {}

		"""set implicit states"""
		self.input_validated = False
		self.directory = source_code_directory

	def _filterDeps(self, filepath, packagepath):
		if packagepath != ".":
			return os.path.dirname(filepath) == packagepath

		return os.path.dirname(filepath) == ""

	def _normalizePath(self, path):
		return path[1:] if path[0] == "/" else path

	def packages(self):
		return self._getProjectPackages()

	def exportedApi(self):
		return self._getProjectExportedAPI()

	def _getProjectPackages(self):
		data = {}

		# package imports
		package_imports = []
		for key in self.package_imports:
			path = str(key.split(":")[0])
			qualifier = str(key.split(":")[1])
			arr = sorted(map(lambda i: str(i), self.package_imports[key]))

			deps = []
			for dep in arr:
				files = filter(lambda l: self._filterDeps(l, path), self.package_imports_occurence[dep])
				# filter out deps of main packages
				files = filter(lambda l: l.split(":")[1] != "main", files)

				files = map(lambda l: os.path.basename(l.split(":")[0]), files)
				# filter out all test files
				files = filter(lambda l: not l.endswith("_test.go"), files)

				if files == []:
					continue

				dep_obj = {
					"name": dep,
					"location": files
				}
				deps.append(dep_obj)

			pkg_obj =  {
				"package": self._normalizePath(path),
				"dependencies": deps,
				"qualifier": qualifier
			}
			package_imports.append(pkg_obj)

		data["dependencies"] = package_imports

		# list of defined packages (defined package has at least one exported symbol)
		data["packages"] = map(lambda i: self._normalizePath(str(i.split(":")[0])), self.symbols.keys())

		# list of tests
		test_objs = []
		for test_dir in self.test_directory_dependencies:
			test_obj = {
				"test": self._normalizePath(test_dir),
				"dependencies": self.test_directory_dependencies[test_dir]
			}
			test_objs.append(test_obj)

		data["tests"] = test_objs

		# files with 'package main'
		main_objs = []
		for filename in self.main_package_deps:
			main_obj = {
				"filename": self._normalizePath(filename),
				"dependencies": self.main_package_deps[filename]
			}
			main_objs.append(main_obj)

		data["main"] = main_objs

		return data

	def _getProjectExportedAPI(self):
		packages = []
		for key in self.symbols:
			package = {}

			# full package name (location of a package without ipprefix)
			path = str(key.split(":")[0])
			package["package"] = self._normalizePath(path)

			# data types
			data_types = []
			for type in self.symbols[key]["types"]:
				c = GoTypeCoder(type)
				data_types.append(c.codeDataType())

			package["datatypes"] = data_types

			# functions
			functions_types = []
			# {u'name': u'Close', u'def': {u'params': [], u'returns': [], u'recv': [{u'type': u'ident', u'def': u'closeWaiter'}]}}
			for fnc in self.symbols[key]["funcs"]:
				c = GoTypeCoder(fnc)
				functions_types.append(c.codeFunctionType())

			package["functions"] = functions_types

			# variables
			vars_types = []
			for var in self.symbols[key]["vars"]:
				c = GoTypeCoder(var)
				vars_types.append(c.codeVariableType())

			package["variables"] = vars_types

			packages.append(package)

		return packages

	def _getGoSymbols(self, path, imports_only=False):
		script_dir = getScriptDir(__file__) + "/."
		options = ""
		if imports_only:
			options = "-imports"

		so, se, rc = runCommand("%s/parseGo %s '%s'" % (script_dir, options, path))
		if rc != 0:
			return (1, se)

		return (0, so)

	def _mergeGoSymbols(self, jsons = []):
		"""
		Exported symbols for a given package does not have any prefix.
		So I can drop all import paths that are file specific and merge
		all symbols.
		Assuming all files in the given package has mutual exclusive symbols.
		"""
		# <siXy> imports are per file, exports are per package
		# on the highest level we have: pkgname, types, funcs, vars, imports.

		symbols = {}
		symbols["types"] = []
		symbols["funcs"] = []
		symbols["vars"]  = []
		for file_json in jsons:
			symbols["types"] += file_json["types"]
			symbols["funcs"] += file_json["funcs"]
			symbols["vars"]  += file_json["vars"]

		return symbols

	def extract(self):
		"""

		"""
		bname = os.path.basename(self.directory)
		go_packages = {}
		ip_packages = {}
		test_directories = []
		test_directory_dependencies = {}
		ip_used = []
		package_imports = {}
		main_packages = []
		main_package_deps = {}

		cme = ContentMetadataExtractor(self.directory)
		cme.extract()

		for dir_info in cme.goDirectories():
			#if sufix == ".":
			#	sufix = bname
			pkg_name = ""
			prefix = ""
			jsons = {}
			for go_file in dir_info['files']:

				if self.verbose:
					logging.warning("Scanning %s..." % ("%s/%s" % (dir_info['dir'], go_file)))

				go_file_json = {}
				err, output = self._getGoSymbols("%s/%s/%s" %
					(self.directory, dir_info['dir'], go_file), self.imports_only)
				if err != 0:
					if self.skip_errors:
						logging.warning("Error parsing %s: %s" % ("%s/%s" % (dir_info['dir'], go_file), output))
						continue
					else:
						raise ExtractionError("Error parsing %s: %s" % ("%s/%s" % (dir_info['dir'], go_file), output))
				else:
					#print go_file
					go_file_json = json.loads(output)

				pname = go_file_json["pkgname"]

				for path in go_file_json["imports"]:
					# filter out all import paths starting with ./
					if path["path"].startswith("./"):
						continue

					# filter out all .. import paths
					if path["path"] == "..":
						continue

					# file_pkg_pair:
					# 1: path to a directory defining a package
					# 2: package NAME actually used in 'package NAME'
					if dir_info['dir'] == ".":
						file_pkg_pair = "%s:%s" % (go_file, pname)
					else:
						file_pkg_pair = "%s/%s:%s" % (dir_info['dir'], go_file, pname)

					if path["path"] not in self.package_imports_occurence:
						self.package_imports_occurence[str(path["path"])] = [str(file_pkg_pair)]
					else:
						self.package_imports_occurence[str(path["path"])].append(str(file_pkg_pair))

					if path["path"] in ip_used:
						continue

					ip_used.append(path["path"])

				# don't check test files, read their import paths only
				if go_file.endswith("_test.go"):
					# get dependencies of tests
					dir_key = dir_info['dir']
					if dir_key not in test_directory_dependencies:
						test_directory_dependencies[dir_key] = []

					test_directory_dependencies[dir_key] = test_directory_dependencies[dir_key] + map(lambda p: str(p["path"]), go_file_json["imports"])
					test_directories.append(dir_info['dir'])
					continue

				# skip all main packages
				if pname == "main":
					if dir_info['dir'] == ".":
						main_key = go_file
					else:
						main_key = "%s/%s" % (dir_info['dir'], go_file)

					main_packages.append(main_key)
					main_package_deps[main_key] = sorted(map(lambda p: str(p["path"]), go_file_json["imports"]))
					continue

				# all files in a directory must define the same package
				if (pkg_name != "" and pkg_name != pname):
					err_msg = "directory %s contains definition of more packages, i.e. %s" % (dir_info['dir'], pname)

					if self.skip_errors:
						logging.error(err_msg)
						continue

					raise ExtractionError(err_msg)

				pkg_name = pname

				# build can contain two different prefixes
				# but with the same package name.
				prefix = dir_info["dir"] + ":" + pkg_name
				i_paths = map(lambda i: i["path"], go_file_json["imports"])
				if prefix not in jsons:
					jsons[prefix] = [go_file_json]
					package_imports[prefix] = i_paths
				else:
					jsons[prefix].append(go_file_json)
					package_imports[prefix] = package_imports[prefix] + i_paths

			#print dir_info["dir"]
			#print dir_info['files']
			#print "#%s#" % pkg_name
			if prefix in jsons:
				go_packages[prefix] = self._mergeGoSymbols(jsons[prefix])
				ip_packages[prefix] = dir_info["dir"]
				package_imports[prefix] = list(set(package_imports[prefix]))

		# sort and unique test dependencies
		for test_key in test_directory_dependencies:
			test_directory_dependencies[test_key] = sorted(set(test_directory_dependencies[test_key]))


		# unique package_imports_occurence
		for path in self.package_imports_occurence:
			self.package_imports_occurence[path] = list(set(self.package_imports_occurence[path]))

		self.symbols = go_packages
		self.symbols_position = ip_packages
		self.package_imports = package_imports
		self.imported_packages = ip_used
		self.test_directories = list(set(test_directories))
		self.test_directory_dependencies = test_directory_dependencies
		self.main_packages = main_packages
		self.main_package_deps = main_package_deps

		return self
