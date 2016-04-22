#
# W.r.t. commit. Commit is relevant only to upstream repositories.
# In a case of distribution provider, each distrubution rpms corresponds to a commit.
# One commit can correspond to more ipprefixes. Commit comes from original upstream revision system.
# Commit's purpose in distribution snapshots is to trace project's origin.
# E.g. it can be used to compare distribution commit with upstream one and decide
# if distribution rpm is outdated.
#

from .projectgithubrepositorycapturer import ProjectGithubRepositoryCapturer
from .projectbitbucketrepositorycapturer import ProjectBitbucketRepositoryCapturer
from lib.repository.repositoryclientbuilder import RepositoryClientBuilder

class ProjectCapturer(object):

	def __init__(self, provider):
		self._signature = {}
		self._provider = provider

	def _validateProvider(self, provider):
		# TODO(jchaloup): use JSON Schema for validation
		if "provider" not in provider:
			raise ValueError("Missing provider property: %s" % str(provider))

	def capture(self, commit = ""):
		"""Capture the current state of a project based on its provider

		Commit is relevant only for upstream providers.
		If empty, the latest commit from provider repository is taken.
		It is ignored for distribution providers.

		:param provider: project provider, e.g. upstream repository, distribution builder
		:type  provider: json/dict
		:param commit: project's original commit
		:type  commit: string
		"""
		self._validateProvider(self._provider)

		# get client for repository
		# TODO(jchaloup): read config file to switch between local and remove clients
		# TODO(jchaloup): remote client can cover gofed infratructure or any remove source for repository info
		client = RepositoryClientBuilder().buildWithRemoteClient(self._provider)

		if self._provider["provider"] == "github":
			self._signature = ProjectGithubRepositoryCapturer(self._provider, client).capture(commit).signature()
		elif self._provider["provider"] == "bitbucket":
			self._signature = ProjectBitbucketRepositoryCapturer(self._provider, client).capture(commit).signature()
		else:
			raise KeyError("Provider '%s' not recognized" % self._provider["provider"])

		return self

	def signature(self):
		return self._signature

