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

class ProjectCapturer(object):

	def __init__(self, provider, client = None):
		self._client = client
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

		if self._provider["provider"] == "github":
			self._signature = ProjectGithubRepositoryCapturer(self._provider, self._client).capture(commit).signature()
		elif self._provider["provider"] == "bitbucket":
			self._signature = ProjectBitbucketRepositoryCapturer(self._provider, self._client).capture(commit).signature()
		else:
			raise KeyError("Provider '%s' not recognized" % self._provider["provider"])

		return self

	def signature(self):
		return self._signature

