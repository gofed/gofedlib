import re
from types import UnsupportedImportPathError

UNKNOWN = 0
GITHUB = 1
GOOGLECODE = 2
GOOGLEGOLANGORG = 3
GOLANGORG = 4
GOPKG = 5
BITBUCKET = 6

# TODO(jchaloup): decompose the parser into generic UrlParser and GoImportPathParser
# so the generic one can be used to generate provider/repository signatures
# and the go one to interpret paths as go packages (e.g. what package is Native, what is prefix, tc.)
# Among other things distinguish go package name generator

# Three use cases for import paths
# 1. get project source code repository url
# 2. decompose import paths into classes (get ipprefix)
# 3. generate package name for project

# For the first I just need ip2pp mapping and ipprefix.
# For the second case I need a list of native import paths and ipprefix.
# For the third I just need ipprefix (it is not repository related)
#

class ImportPathParser(object):
	"""
	Parses information from given
	import path:
		provider
		project
		repository
		prefix
	"""

	def __init__(self, ip2pp_mapping = {}, ip2pkg_mapping = {}, native_packages = []):
		"""
		:param ip2pp_mapping: import path prefix to provider prefix mapping
		:type  ip2pp_mapping: json
		:param ip2pkg_mapping: import path prefix to package name mapping
		:type  ip2pkg_mapping: json
		:param native_packages: list of golang native packages
		:type  native_packages: json
		"""
		self.ip2pp_mapping = ip2pp_mapping
		self.ip2pkg_mapping = ip2pkg_mapping
		self.native_packages = native_packages

		self.provider = UNKNOWN
		self.provider_name = ""
		self.provider_prefix = ""
		self.project = ""
		self.repository = ""
		self.prefix = ""
		self.native = False
		self.import_path_prefix = ""
		self.provider_signature = {}

	def getProvider(self):
		return self.provider

	def getProject(self):
		return self.project

	def getRepository(self):
		return self.repository

	def getPrefix(self):
		return self.prefix

	def getProviderPrefix(self):
		return self.provider_prefix

	def getProviderName(self):
		return self.provider_name

	def getProviderSignature(self):
		return self.provider_signature

	def getImportPathPrefix(self):
		return self.import_path_prefix

	def isNative(self):
		return self.native

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

	def parse(self, importpath):
		""" Parse import path into provider, project, repository
		and other recognizable parts

		:param importpath:	import path to parse
		:type  importpath:	str
		:return: bool
		"""
		# reset nativness
		self.native = False

		url = re.sub(r'http://', '', importpath)
		url = re.sub(r'https://', '', url)

		# is import path native package?
		if importpath.split('/')[0] in self.native_packages:
			self.native = True
			return self

		# any ip customization before parsing?
		custom_ip = self.detectCustomImportPaths(url)
		if custom_ip != {}:
			url = custom_ip["provider_prefix"]
			# get ipprefix of the original import path
			self.import_path_prefix = custom_ip["prefix"]
		else:
			info = self._parsePrefix(url)
			self.import_path_prefix = info["prefix"]

		info = self._parsePrefix(url)

		self.provider = info["provider"]
		self.project = info["project"]
		self.repository = info["repo"]
		self.provider_prefix = info["provider_prefix"]
		self.provider_name = info["provider_name"]
		self.provider_signature = info["provider_signature"]

		if custom_ip != {}:
			self.prefix = custom_ip["prefix"]
		else:
			self.prefix = info["prefix"]

		return self

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
		repo["provider"] = GITHUB
		repo["project"] = parts[1]
		repo["repo"] = parts[2]
		repo["prefix"] = "/".join(parts[:3])
		repo["provider_prefix"] = "github.com/%s/%s" % (parts[1], parts[2])
		repo["provider_name"] = "github"
		repo["provider_signature"] = {"provider": "github", "username": repo["project"], "project": repo["repo"]}

		return repo

	def parseGooglecodeImportPath(self, path):
		"""
		Definition: code.google.com/p/<repo>
		"""
		parts = path.split("/")

		if len(parts) < 3:
			raise ValueError("Import path %s is not in code.google.com/p/ form" % path)

		repo = {}
		repo["provider"] = GOOGLECODE
		repo["project"] = parts[1]
		repo["repo"] = parts[2]
		repo["prefix"] = "/".join(parts[:3])
		repo["provider_prefix"] = "code.google.com/p/%s" % (parts[2])
		repo["provider_name"] = "googlecode"
		repo["provider_signature"] = {"provider": "googlecode", "username": repo["project"], "project": repo["repo"]}

		return repo

	def parseBitbucketImportPath(self, path):
		"""
		Definition: bitbucket.org/<project>/<repo>
		"""
		parts = path.split("/")

		if len(parts) < 3:
			raise ValueError("Import path %s is not in bitbucket.org/<project>/<repo> form" % path)

		repo = {}
		repo["provider"] = BITBUCKET
		repo["project"] = parts[1]
		repo["repo"] = parts[2]
		repo["prefix"] = "/".join(parts[:3])
		repo["provider_prefix"] = "bitbucket.org/%s/%s" % (parts[1], parts[2])
		repo["provider_name"] = "bitbucket"
		repo["provider_signature"] = {"provider": "bitbucket", "username": repo["project"], "project": repo["repo"]}

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
			prefix = "/".join(parts[:3])
			provider_prefix = "gopkg.in/%s/%s" % (parts[1], parts[2])
		else:
			if len(parts) < 2:
				raise ValueError("Import path %s is not in gopkg.in/<repo>.<v> form" % path)

			prefix = "/".join(parts[:2])
			dotparts = parts[1].split(".")
			if len(dotparts) == 1:
				# gopkg.in/<project>/<repo>
				if len(parts) != 3:
					raise ValueError("Import path %s is not in gopkg.in/<project>/<repo> form" % path)
				project = parts[1]
				repository = parts[2]
				provider_prefix = "gopkg.in/%s/%s" % (parts[1], parts[2])

			else:
				if len(dotparts) != 2:
					raise ValueError("Import path %s is not in gopkg.in/<repo>.<v> form" % path)

				project = ""
				repository = dotparts[0]
				provider_prefix = "gopkg.in/%s.%s" % (dotparts[0], dotparts[1])

		repo = {}
		repo["provider"] = GOPKG
		repo["project"] = ""
		repo["repo"] = repository
		repo["prefix"] = prefix
		repo["provider_prefix"] = provider_prefix
		repo["provider_name"] = "gopkg"
		repo["provider_signature"] = {"provider": "gopkg", "username": repo["project"], "project": repo["repo"]}

		return repo

	def parseGooglegolangImportPath(self, path):
		"""
		Definition:  google.golang.org/<repo>
		"""
		parts = path.split("/")

		if len(parts) < 2:
			raise ValueError("Import path %s is not in google.golang.org/<repo> form" % path)

		repo = {}
		repo["provider"] = GOOGLEGOLANGORG
		repo["project"] = ""
		repo["repo"] = parts[1]
		repo["prefix"] = "/".join(parts[:2])
		repo["provider_prefix"] = "google.golang.org/%s" % (parts[1])
		repo["provider_name"] = "googlegolangorg"
		repo["provider_signature"] = {"provider": "googlegolangorg", "username": repo["project"], "project": repo["repo"]}

		return repo

	def parseGolangorgImportPath(self, path):
		"""
		Definition:  golang.org/x/<repo>
		"""
		parts = path.split("/")

		if len(parts) < 3:
			raise ValueError("Import path %s is not in golang.org/x/<repo> form" % path)

		repo = {}
		repo["provider"] = GOLANGORG
		repo["project"] = ""
		repo["repo"] = parts[2]
		repo["prefix"] = "/".join(parts[:3])
		repo["provider_prefix"] = "golang.org/x/%s" % (parts[2])
		repo["provider_name"] = "golangorg"
		repo["provider_signature"] = {"provider": "golangorg", "username": repo["project"], "project": repo["repo"]}

		return repo

	def detectCustomImportPaths(self, path):
		"""
		Some import paths does not reflect provider prefix
		e.g. camlistore.org/pkg/googlestorage is actually at
		github.com/camlistore/camlistore repository under
		pkg/googlestorage directory.
		"""
		for assignment in self.ip2pp_mapping:
			if path.startswith(assignment["ipprefix"]):
				return {"prefix": assignment["ipprefix"], "provider_prefix": assignment["provider_prefix"]}

		return {}

	def getPackageName(self):
		"""
		Package name construction is based on provider, not on prefix.
		Prefix does not have to equal provider_prefix.
		"""
		for assignment in self.ip2pkg_mapping:
			if assignment["ipprefix"] == self.prefix:
				return assignment["package"]

		if self.provider == GITHUB:
			return self.github2pkgdb(self.project, self.repository)
		if self.provider == BITBUCKET:
			return self.bitbucket2pkgdb(self.project, self.repository)
		if self.provider == GOOGLECODE:
			return self.googlecode2pkgdb(self.repository)
		if self.provider == GOOGLEGOLANGORG:
			return self.googlegolangorg2pkgdb(self.repository) 
		if self.provider == GOLANGORG:
			return self.golangorg2pkgdb(self.repository)
		if self.provider == GOPKG:
			return self.gopkg2pkgdb(self.repository)

		raise ValueError("Provider not supported")

	def github2pkgdb(self, project, repository):
		# github.com/<project>/<repository>
		return "golang-github-%s-%s" % (project, repository)

	def bitbucket2pkgdb(self, project, repository):
		# bitbucket.org/<project>/<repository>
		return "golang-bitbucket-%s-%s" % (project, repository)

	def googlecode2pkgdb(self, repository):
		# code.google.com/p/<repository>
		# rotate the repo name
		nparts = repository.split('.')
		if len(nparts) > 2:
			raise ValueError("%s repo contains more than one dot in its name, not implemented" % repository)

		if len(nparts) == 2:
			return "golang-googlecode-%s" % (nparts[1] + "-" + nparts[0])
		else:
			return "golang-googlecode-%s" % repository
	       
	def googlegolangorg2pkgdb(self, repository):
		# google.golang.org/<repository>
		return "golang-google-golangorg-%s" % repository

	def golangorg2pkgdb(self, repository):
		# golang.org/x/<repo>
		return "golang-golangorg-%s" % repository

	def gopkg2pkgdb(self, repository):
		# only gopkg.in/<v>/<repo>
		# or   gopkg.in/<repo>.<v>
		return "golang-gopkg-%s" % repository

