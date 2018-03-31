import json
import yaml
from gofedlib.go.importpath.decomposerbuilder import ImportPathsDecomposerBuilder
import datetime
import pytz

class Snapshot(object):

	def __init__(self):
		self._packages = {}

	def clear(self):
		self._packages = {}
		return self

	def addPackage(self, package, commit):
		self._packages[package] = commit
		return self

	def packages(self):
		# TODO(jchaloup): introduce iterator instead
		return self._packages

	def Godeps(self):
		"""Return the snapshot in Godeps.json form
		"""
		dict = []
		for package in sorted(self._packages.keys()):
			dict.append({
				"ImportPath": str(package),
				"Rev": str(self._packages[package])
			})

		return dict

	def GLOGFILE(self):
		"""Return the snapshot in GLOGFILE form
		"""
		lines = []
		for package in sorted(self._packages.keys()):
			lines.append("%s %s" % (str(package), str(self._packages[package])))

		return "\n".join(lines)

	def Glide(self):
		"""Return the snapshot in glide.lock form
		"""
		dict = {
			"hash": "???",
			"updated": str(datetime.datetime.now(tz=pytz.utc).isoformat()),
			"imports": [],
		}

		decomposer = ImportPathsDecomposerBuilder().buildLocalDecomposer()
		decomposer.decompose(self._packages.keys())
		classes = decomposer.classes()

		for ipp in classes:
			dep = {
				"name": ipp,
				"version": str(self._packages[classes[ipp][0]])
			}
			if len(classes[ipp]) > 1 or classes[ipp][0] != ipp:
				dep["subpackages"] = map(lambda l: l[len(ipp)+1:], classes[ipp])

			dict["imports"].append(dep)

		return yaml.dump(dict, default_flow_style=False)

	def readGodepsFile(self, file):
		with open(file, "r") as f:
			data = json.load(f)

		# Deps key?
		if "Deps" not in data:
			raise ValueError("Deps key missing in %s" % file)

		packages = {}
		for package in data["Deps"]:
			if "ImportPath" not in package:
				raise ValueError("ImportPath key missing in %s" % file)

			if "Rev" not in package:
				raise ValueError("Rev key missing in %s" % file)

			packages[package["ImportPath"]] = package["Rev"]

		# The file is valid Godeps.json file
		self.clear()
		self._packages = packages

		return self

	def readGLOGFILE(self, file):
		raise NotImplementedError()
		with open(file, "r") as f:
			data = json.load(f)

	def readGlideLockFile(self, file):
		with open(file, "r") as f:
			data = yaml.load(f)

		if "imports" in data:
			imported_pkgs = data["imports"]
		else:
			raise ValueError("imports key missing in %s" % file)

		packages = {}
		for package in imported_pkgs:
			for key in ["name", "version"]:
				if key not in package:
					raise ValueError("package key missing in import array item in %s" % file)

			if "subpackages" in package:
				for subpkg in package["subpackages"]:
					packages["%s/%s" % (package["name"], subpkg)] = package["version"]
			else:
				packages[package["name"]] = package["version"]

		self.clear()
		self._packages = packages

		return self

        def readVendorFile (self, file):
            with open(file,"r") as f:
                data = json.load(f)

            if "package" not in data:
                raise ValueError("package key missing in %s" % file)

            packages = {}

            for package in data["package"]:
                if "path" not in package:
                    raise ValueError("Import path missing in %s" % file)
                if "revision" not in package:
                    raise ValueError("Revision missing in %s" % file)

                packages[package["path"]] = package["revision"]

            self.clear()
            self._packages = packages

            return self
