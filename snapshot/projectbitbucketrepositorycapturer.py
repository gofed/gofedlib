from .projectsnapshotcapturer import ProjectSnapshotCapturer
from lib.types import CommitNotRetrieved
from lib.urlbuilder import UrlBuilder

class ProjectBitbucketRepositoryCapturer(ProjectSnapshotCapturer):

	def __init__(self, client = None):
		# TODO(jchaloup): inject repository client instead of calling local _getGithubLatestCommit
		self._client = client
		self._commit = ""
		self._provider = {}
		self._resource_url = ""

	def capture(self, provider, commit = ""):
		# even if an exception get thrown, you don't lost commit from the previous capture
		if commit == "":
			commit = self._getBitbucketLatestCommit(provider["username"], provider["project"])

		self._commit = commit
		self._resource_url = UrlBuilder().buildBitbucketSourceCodeTarball(provider["username"], provider["project"], commit)

	def signature(self):
		return {
			"provider": self._provider,
			"commit": self._commit,
			"resource_url": self._resource_url
		}

	def _getLatestCommit(self, username, project):
		"""
		:param username:	bitbucket username
		:type  username:	str
		:param project:		bitbucket project
		:type  project:		str
		"""
		resource_url = "https://bitbucket.org/api/1.0/repositories/%s/%s/changesets?limit=1" % (username, project)
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

