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

class ProjectCapturer(self):

	def __init__(self):
		self._signature = {}

	def _validateProvider(self, provider):
		# TODO(jchaloup): use JSON Schema for validation
		if "provider" not in provider:
			raise ValueError("Missing provider property: %s" % str(provider))

	def capture(provider, commit = ""):
		"""Capture the current state of a project based on its provider

		Commit is relevant only for upstream providers.
		If empty, the latest commit from provider repository is taken.
		It is ignored for distribution providers.

		:param provider: project provider, e.g. upstream repository, distribution builder
		:type  provider: json/dict
		:param commit: project's original commit
		:type  commit: string
		"""
		self._validateProvider(provider)

		if provider["provider"] == "github":
			self._signature = ProjectGithubRepositoryCapturer().capture(provider, commit).signature()
		elif provider["provider"] == "bitbucket":
			self._signature = ProjectBitbucketRepositoryCapturer().capture(provider, commit).signature()
		else:
			raise KeyError("Provider '%s' not recognized" % provider["provider"])

		return self

	def signature(self):
		return self._signature

	def _getResource(self, resource_url):
		try:
			return urllib2.urlopen(resource_url)
		except urllib2.URLError as err:
			msg = "Unable to retrieve resource, url = %s, err = " % (resource_url, err)
			raise urllib2.URLError(msg)
		except urllib2.HTTPError as err:
			msg = "Unable to retrieve resource, url = %s, err = " % (resource_url, err)
			raise urllib2.HTTPError(msg)

