from .projectsnapshotcapturer import ProjectSnapshotCapturer
from lib.types import CommitNotRetrieved
from lib.urlbuilder.builder import UrlBuilder

class ProjectGithubRepositoryCapturer(ProjectSnapshotCapturer):

	def __init__(self, provider, client = None):
		# TODO(jchaloup): inject repository client instead of calling _getLatestCommit
		self._client = client
		self._commit = ""
		self._provider = provider
		self._resource_url = ""

	def capture(self, commit = ""):
		# even if an exception get thrown, you don't lost commit from the previous capture
		if commit == "":
			commit = self._client.latestCommit()

		self._commit = commit
		self._resource_url = UrlBuilder().buildGithubSourceCodeTarball(
			self._provider["username"],
			self._provider["project"],
			commit
		)

		return self

	def signature(self):
		return {
			"provider": self._provider,
			"commit": self._commit,
			"resource_url": self._resource_url
		}

