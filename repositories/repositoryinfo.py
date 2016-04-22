import urllib2
import json
from importpathparser import GITHUB, BITBUCKET
from types import CommitNotRetrieved

class ArchiveInfo(object):
	"""
	Class to represent information about
	archive:
		shortcommit - auxiliary value
		archive - tar.gz, zip, ...
		archive_dir - extracted archive's directory
		archive_url - download url
	"""

	def __init__(self):
		self._archive = ""

	@property
	def shortcommit(self):
		return self._shortcommit

	@shortcommit.setter
	def shortcommit(self, value):
		self._shortcommit = value

	@property
	def archive(self):
		return self._archive

	@archive.setter
	def archive(self, value):
		self._archive = value

	@property
	def archive_dir(self):
		return self._archive_dir

	@archive_dir.setter
	def archive_dir(self, value):
		self._archive_dir = value

	@property
	def archive_url(self):
		return self._archive_url

	@archive_url.setter
	def archive_url(self, value):
		self._archive_url = value

# TODO(jchaloup): replace ipparser with a generic url parser
# so it can be applied not just to golang import paths but to a general repository url
#
# TODO(jchaloup): decompose the code to GithubRepositoryInfo and BitbucketRepositoryInfo
# then build RepositoryInfo over it which get instantiated based on provider signature
# that comes from generic url parser
#
# GitRepoInfo:
# - latest commit
# - tags, labels
#
# GithubInfo
# - releases
# - archive info (tarball name, url)
# 
# Proposed classes:
# git:
# - GitRepositoryInfo,
# - GithubRepositoryInfo
# hg:
# - MercurialRepositoryInfo
# - BitbucketRepositoryInfo

class RepositoryInfo:
	"""Based on given import path and commit (optional) retrieve information
	about repository:
		provider - github, googlecode, bitbucket
		project - repository project, not golang project
		project's repository
		commit
		archive
	The class does not provide methods for downloading resources from a repository.
	It provides methods to construct location of resources, e.g. source code tarball url.

	TODO(jchaloup): maybe return object with data instead of calling class' methods?
	Like response() or info() or make RepositoryInfo product of different class.
	"""
	def __init__(self, ipparser):
		"""
		:param ipparser:	import path parser
		:type  ipparser:	ImportPathParser
		"""
		self.ipparser = ipparser

		self.archive_info = None
		self.signature = ""
		self.commit = ""

	def getCommit(self):
		return self.commit

	def getArchiveInfo(self):
		return self.archive_info

	def retrieve(self, import_path, commit = ""):
		# parse import path
		self.ipparser.parse(import_path)
		
		provider = self.ipparser.getProvider()
		project = self.ipparser.getProject()
		repo = self.ipparser.getRepository()

		# do we know provider?
		if self.commit == "" and provider not in [GITHUB, BITBUCKET]:
			raise ValueError("Latest commit can be detected only for github.com and bitbucket.org")

		# do we have a commit?
		if self.commit == "":
			self.commit = self.getLatestCommit(provider, project, repo)

		self.archive_info = self.constructArchiveInfo(provider, project, repo, self.commit)

		# construct signature
		self.signature = "%s-%s-%s-%s" % (self.ipparser.getProviderName(), project, repo, self.commit)

		return self

	def constructArchiveInfo(self, provider, project, repo, commit):
		# TODO(jchaloup): use UrlBuilder to build urls in the capturer
		if provider == GITHUB:
			shortcommit = commit[:7]
			archive = "%s-%s.tar.gz" % (repo, shortcommit)
			archive_dir = "%s-%s" % (repo, commit)
			archive_url = "https://github.com/%s/%s/archive/%s/%s" % (project, repo, commit, archive)
		elif provider == BITBUCKET:
			shortcommit = commit[:12]
			archive = "%s.tar.gz" % (shortcommit)
			archive_dir = "%s-%s-%s" % (project, repo, shortcommit)
			archive_url = "https://bitbucket.org/%s/%s/get/%s" % (project, repo, archive)
		elif provider == GOOGLECODE:
			shortcommit = commit[:12]
			archive = "%s.tar.gz" % (commit)
			archive_dir = "%s-%s" % (repo, shortcommit)
			# https://go-charset.googlecode.com/archive/ebbeafdc430eb6c7e44e9a730a38eaff4c56ba3a.tar.gz
			archive_url = "https://%s.googlecode.com/archive/%s" % (repo, archive)

		else:
			raise ValueError("Unable to construct archive info: provider not supported")

		archive_info = ArchiveInfo()
		archive_info.shortcommit = shortcommit
		archive_info.archive = archive
		archive_info.archive_dir = archive_dir
		archive_info.archive_url = archive_url

		return archive_info

	def getLatestCommit(self, provider, project, repo):
		"""Retrieve tarball with source codes from a repository
		:param provider:	repository provider
		:type  provider:	str
		:param project:		repository project
		:type  project:		str
		:param repo:		repository
		:type  str:		str
		"""
		if provider == GITHUB:
			return self.getGithubLatestCommit(project, repo)
		if provider == BITBUCKET:
			return self.getBitbucketLatestCommit(project, repo)

		raise ValurError("Unable to retrieve latest commit. Repository provider not supported.")

	def _getResource(self, resource_url):
		try:
			return urllib2.urlopen(resource_url)
		except urllib2.URLError as err:
			msg = "Unable to retrieve resource, url = %s, err = " % (resource_url, err)
			raise urllib2.URLError(msg)
		except urllib2.HTTPError as err:
			msg = "Unable to retrieve resource, url = %s, err = " % (resource_url, err)
			raise urllib2.HTTPError(msg)

	def getGithubLatestCommit(self, project, repo):
		"""
		:param project:		github project
		:type  project:		str
		:param repo:		github repository
		:type  repo:		str
		"""
		resource_url = "https://api.github.com/repos/%s/%s/commits" % (project, repo)
		c_file = self._getResource(resource_url).read()

		# get the latest commit
		commits = json.loads(c_file)
		if type(commits) != type([]):
			if type(commits) == type({}) and 'message' in commits:
				raise CommitNotRetrieved("Latest github commit not retrieved: %s" % commits['message'])

		if len(commits) == 0:
			raise CommitNotRetrieved("Latest github commit not retrieved: no commit found")

		if "sha" not in commits[0]:
			raise CommitNotRetrieved("Latest github commit not retrieved: sha missing")

		return commits[0]["sha"]

	def getBitbucketLatestCommit(self, project, repo):
		resource_url = "https://bitbucket.org/api/1.0/repositories/%s/%s/changesets?limit=1" % (project, repo)
		c_file = self._getResource(resource_url).read()

		# get the latest commit
		data = json.loads(c_file)
		if 'changesets' not in data:
			raise CommitNotRetrieved("Latest bitbucket commit not retrieved: changesets missing")

		commits = data['changesets']
		if type(commits) != type([]):
			raise CommitNotRetrieved("Latest bitbucket commit not retrieved: invalid changeset")

		if len(commits) == 0:
			raise CommitNotRetrieved("Latest bitbucket commit not retrieved: no commit found")

		if 'raw_node' not in commits[0]:
			raise CommitNotRetrieved("Latest bitbucket commit not retrieved: invalid commit")

		return commits[0]["raw_node"]

	def getGithubReleases(self, project, repo):
		resource_url = "https://api.github.com/repos/%s/%s/releases" % (project, repo)
		c_file = self._getResource(resource_url).read()

		# get the latest commit
		releases = []
		for release in json.loads(c_file):
			releases.append(release["tag_name"])

		return releases

	def getGithubTags(self, project, repo):
		resource_url = "https://api.github.com/repos/%s/%s/tags" % (project, repo)
		c_file = self._getResource(resource_url).read()

		data = json.loads(c_file)
		if type(data) == {} and "message" in data:
			raise TagsNotRetrieved("Unable to retrieve tags: %s" % data["message"])

		# get the latest commit
		tags = []
		for tag in data:
			tags.append(tag["name"])

		return tags

	def getSignature(self):
		return self.signature
