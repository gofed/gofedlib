import re
from lib.types import UnsupportedImportPathError

UNKNOWN = 0
GITHUB = 1
GOOGLECODE = 2
GOOGLEGOLANGORG = 3
GOLANGORG = 4
GOPKG = 5
BITBUCKET = 6

class UpstreamProvider(object):

	def __init__(self, ip2pp_mapping = []):
		self.ip2pp_mapping = ip2pp_mapping

		self._prefix = ""
		self._signature = ""

	def parse(self, prefix):
		""" Parse import path into provider, project, repository
		and other recognizable parts

		:param importpath:	import path to parse
		:type  importpath:	str
		:return: bool
		"""
		# reset to default values
		self._prefix = ""

		url = re.sub(r'http://', '', prefix)
		url = re.sub(r'https://', '', url)

		# any prefix customization before parsing?
		custom_prefix = self.detectCustomImportPaths(url)
		if custom_prefix != {}:
			url = custom_prefix["provider_prefix"]

		info = self._parsePrefix(url)

		self._signature = info["signature"]
		self._prefix = info["prefix"]

		return self

	def signature(self):
		return self._signature

	def prefix(self):
		return self._prefix

	def detectCustomImportPaths(self, prefix):
		"""
		Some prefixes does not reflect provider prefix
		e.g. camlistore.org/pkg/googlestorage is actually at
		github.com/camlistore/camlistore repository under
		pkg/googlestorage directory.
		"""
		for assignment in self.ip2pp_mapping:
			if prefix.startswith(assignment["ipprefix"]):
				return {"prefix": assignment["ipprefix"], "provider_prefix": assignment["provider_prefix"]}

		return {}

	def _parsePrefix(self, url):
		repo = self.detectKnownRepo(url)

		if repo == GITHUB:
			return self.parseGithubImportPath(url)
		if repo == GOOGLECODE:
			return self.parseGooglecodeImportPath(url)
		if repo == BITBUCKET:
			return self.parseBitbucketImportPath(url)
		if repo == GOPKG:
			return self.parseGopkgImportPath(url)
		if repo == GOOGLEGOLANGORG:
			return self.parseGooglegolangImportPath(url)
		if repo == GOLANGORG:
			return self.parseGolangorgImportPath(url)

		raise UnsupportedImportPathError("Import path %s not supported" % url)

	def detectKnownRepo(self, url):
		"""
		For given import path detect provider.
		"""
		if url.startswith('github.com'):
			return GITHUB
		if url.startswith('code.google.com/p'):
			return GOOGLECODE
		if url.startswith('golang.org/x'):
			return GOLANGORG
		if url.startswith('gopkg.in'):
			return GOPKG
		if url.startswith('bitbucket.org'):
			return BITBUCKET
		if url.startswith('google.golang.org'):
			return GOOGLEGOLANGORG

		return UNKNOWN

	def parseGithubImportPath(self, path):
		"""
		Definition: github.com/<project>/<repo>
		"""
		parts = path.split("/")

		if len(parts) < 3:
			raise ValueError("Import path %s not in github.com/<project>/<repo> form" % path)

		repo = {}
		repo["prefix"] = "/".join(parts[:3])
		repo["signature"] = {"provider": "github", "username": parts[1], "project": parts[2]}

		return repo

	def parseGooglecodeImportPath(self, path):
		"""
		Definition: code.google.com/p/<repo>
		"""
		parts = path.split("/")

		if len(parts) < 3:
			raise ValueError("Import path %s is not in code.google.com/p/ form" % path)

		repo = {}
		repo["prefix"] = "/".join(parts[:3])
		repo["signature"] = {"provider": "googlecode", "username": "", "project": parts[2]}

		return repo

	def parseBitbucketImportPath(self, path):
		"""
		Definition: bitbucket.org/<project>/<repo>
		"""
		parts = path.split("/")

		if len(parts) < 3:
			raise ValueError("Import path %s is not in bitbucket.org/<project>/<repo> form" % path)

		repo = {}
		repo["prefix"] = "/".join(parts[:3])
		repo["signature"] = {"provider": "bitbucket", "username": parts[1], "project": parts[2]}

		return repo

	def parseGopkgImportPath(self, path):
		"""
		Definition: gopkg.in/<v>/<repo> || gopkg.in/<repo>.<v> || gopkg.in/<project>/<repo>
		"""
		parts = path.split('/')
		if re.match('v[0-9]+', parts[1]):
			if len(parts) < 3:
				raise ValueError("Import path %s is not in gopkg.in/<v>/<repo> form" % path)

			project = ""
			repository = parts[2]
			version = parts[1]
			prefix = "/".join(parts[:3])
			provider_prefix = "gopkg.in/%s/%s" % (parts[1], parts[2])
		else:
			if len(parts) < 2:
				raise ValueError("Import path %s is not in gopkg.in/[<repo>.<v>|<project>/<repo>] form" % path)

			dotparts = parts[1].split(".")
			if len(dotparts) == 1:
				# gopkg.in/<project>/<repo>
				if len(parts) != 3:
					raise ValueError("Import path %s is not in gopkg.in/<project>/<repo> form" % path)
				prefix = "/".join(parts[:3])
				project = parts[1]
				dotparts = parts[2].split(".")
				repository = dotparts[0]
				if len(dotparts) == 0:
					version = ""
				else:
					version = dotparts[1]

				provider_prefix = "gopkg.in/%s/%s" % (parts[1], parts[2])

			else:
				if len(dotparts) != 2:
					raise ValueError("Import path %s is not in gopkg.in/<repo>.<v> form" % path)
				prefix = "/".join(parts[:2])
				project = ""
				repository = dotparts[0]
				version = dotparts[1]
				provider_prefix = "gopkg.in/%s" % parts[1]

		repo = {}
		repo["prefix"] = prefix
		repo["signature"] = {"provider": "gopkg", "username": project, "project": repository, "version": version}

		return repo

	def parseGooglegolangImportPath(self, path):
		"""
		Definition:  google.golang.org/<repo>
		"""
		parts = path.split("/")

		if len(parts) < 2:
			raise ValueError("Import path %s is not in google.golang.org/<repo> form" % path)

		repo = {}
		repo["prefix"] = "/".join(parts[:2])
		repo["signature"] = {"provider": "googlegolangorg", "username": "", "project": parts[1]}

		return repo

	def parseGolangorgImportPath(self, path):
		"""
		Definition:  golang.org/x/<repo>
		"""
		parts = path.split("/")

		if len(parts) < 3:
			raise ValueError("Import path %s is not in golang.org/x/<repo> form" % path)

		repo = {}
		repo["prefix"] = "/".join(parts[:3])
		repo["signature"] = {"provider": "golangorg", "username": "", "project": parts[2]}

		return repo

