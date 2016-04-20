import json
import re

class PackageNameGenerator(object):

	def __init__(self, s2n_mapping = []):
		self.s2n_mapping = s2n_mapping
		self._name = ""

	def generate(self, project):
		"""
		Package name construction is based on provider, not on prefix.
		Prefix does not have to equal provider_prefix.
		"""
		for assignment in self.s2n_mapping:
			if assignment["ipprefix"] == project:
				self._name = assignment["package"]
				return self

		#
		# github.com -> github
		# code.google.com/p/ -> googlecode
		# golang.org/x/ -> golangorg
		# gopkg.in/check.v1 -> gopkg-check
		# camlistore.org
		#

		name = project
		if name.startswith("github.com"):
			name = re.sub(r"^github\.com", "github", name)

		if name.startswith("gopkg.in"):
			name = re.sub(r"gopkg\.in", "gopkg", name)
			# any version marks?
			name = re.sub(r"\.v\d", "", name)
			name = re.sub(r"/v\d/", "/", name)

		if name.startswith("code.google.com/p"):
			name = re.sub(r"^code\.google\.com/p", "googlecode", name)

		if name.startswith("golang.org/x"):
			name = re.sub(r"^golang\.org/x", "golangorg", name)

		if name.startswith("google.golang.org"):
			name = re.sub(r"^google\.golang\.org", "googlegolangorg", name)

		if name.startswith("bitbucket.org"):
			name = re.sub(r"^bitbucket\.org", "bitbucket", name)

		if name.startswith("k8s.io"):
			name = re.sub(r"^k8s\.io", "k8s", name)

		if name.endswith(".org"):
			name = re.sub(r"\.org$", "", name)

		name = name.replace("/", "-")

		self._name = "golang-%s" % name

		return self

	def name(self):
		return self._name

if __name__ == "__main__":
	with open("import_path_to_package_name_mapping.json", "r") as f:
		mapping = json.load(f)

	g = PackageNameGenerator(mapping)

	print g.generate("gopkg.in/check.v1").name()
	g.generate("github.com/coreos/etcd")
	g.generate("gopkg.in/v1/check")
	g.generate("gopkg.in/natefinch/lumberjack.v1")
