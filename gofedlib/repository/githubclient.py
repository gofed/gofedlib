# https://developer.github.com/v3/

from github import Github, GithubException
import time
import datetime
import requests

class GithubClient(object):

	def __init__(self, username, project):
		self._username = username
		self._project = project
		self.github = Github()
		try:
			self.repo = self.github.get_repo(username + '/' + project)
		except GithubException as e:
			raise KeyError('Failed to get repository information: ' % e)

	def branches(self):
		"""Return a list of branches for given repository

		Raises GithubException if rate limit is exceeded

		:return: [str]
		"""
		if self.github.get_rate_limit().rate.limit == 0:
			raise GithubException

		branches = self.repo.get_branches()
		return [x.name for x in branches]

	def _commitData(self, commit):
		"""Get data from a commit object

		:param commit: commit object
		:type  commit: github.Commit.Commit
		"""
		return {
			"hexsha": commit.sha,
			"adate": time.mktime(commit.commit.author.date.timetuple()),
			"cdate": time.mktime(commit.commit.committer.date.timetuple()),
			"author": "%s <%s>" % (commit.commit.author.name, commit.commit.author.email),
			"message": commit.commit.message
		}

	def commits(self, branch, since=0, to=int(time.time()) + 86400):
		"""For given branch return a list of commits.
		Each commit contains basic information about itself.

		Raises GithubException if rate limit is exceeded

		:param branch: git branch
		:type  branch: str
		:param since: minimal timestamp for commit's commit date
		:type  since: int
		:param to: maximal timestamp for commit's commit date
		:type  to: int
		"""
		if self.github.get_rate_limit().rate.limit == 0:
			raise GithubException

		commits = {}
		since_dt = datetime.datetime.fromtimestamp(since)
		to_dt = datetime.datetime.fromtimestamp(to)
		for commit in self.repo.get_commits(sha=branch, since=since_dt, until=to_dt):
			commits[commit.sha] = self._commitData(commit)
		return commits

	def commit(self, commit):
		"""Get data for a given commit

		Raises KeyError if a commit is not found or not parsed.

		:param commit: repository commit
		:type  commit: string
		"""
		try:
			return self._commitData(self.repo.get_commit(commit))
		except (ValueError, KeyError, GithubException):
			raise KeyError("Commit %s not found" % commit)

	def latestCommit(self):
		for commit in self.repo.get_commits():
			return self._commitData(commit)

		raise KeyError("Latest commit not found")

	def _getResource(self, resource_url):
		r = requests.get(resource_url)
		if r.status_code != requests.codes.ok:
			raise GithubException("Unable to retrieve resource")

		return r.json()

	def releases(self):
		# TODO(jchaloup): not tested, test!!!
		resource_url = "https://api.github.com/repos/%s/%s/releases" % (self._username, self._project)
		data = self._getResource(resource_url)

		# get the latest commit
		releases = []
		for release in data:
			releases.append(release["tag_name"])

		return releases

	def tags(self):
		# TODO(jchaloup): not tested, test it!!!, e.g. TagsNotRetrieved is not defined
		resource_url = "https://api.github.com/repos/%s/%s/tags" % (self._username, self._project)
		data = self._getResource(resource_url)
		if type(data) == {} and "message" in data:
			raise TagsNotRetrieved("Unable to retrieve tags: %s" % data["message"])

		# get the latest commit
		tags = []
		for tag in data:
			tags.append(tag["name"])

		return tags

