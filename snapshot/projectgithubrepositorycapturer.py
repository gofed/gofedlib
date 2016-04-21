from .projectsnapshotcapturer import ProjectSnapshotCapturer
from lib.types import CommitNotRetrieved
from lib.urlbuilder import UrlBuilder

class ProjectGithubRepositoryCapturer(ProjectSnapshotCapturer):

	def __init__(self, client = None):
		# TODO(jchaloup): inject repository client instead of calling _getLatestCommit
		self._client = client
		self._commit = ""
		self._provider = {}
		self._resource_url = ""

	def capture(self, provider, commit = ""):
		# even if an exception get thrown, you don't lost commit from the previous capture
		if commit == "":
			commit = self._getLatestCommit(provider["username"], provider["project"])

		self._commit = commit
		self._resource_url = UrlBuilder().buildGithubSourceCodeTarball(provider["username"], provider["project"], commit)

	def signature(self):
		return {
			"provider": self._provider,
			"commit": self._commit,
			"resource_url": self._resource_url
		}

	def _getLatestCommit(self, username, project):
		"""
		:param username:	github username
		:type  username:	str
		:param project:		github project
		:type  project:		str
		"""
		# TODO(jchaloup): move the code to github repository client (or use the code from it)
		resource_url = "https://api.github.com/repos/%s/%s/commits" % (upstream, project)
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

