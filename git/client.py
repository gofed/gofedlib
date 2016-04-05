#
# All communication with github.com, its remote positories
# or local ones will be carried through this module and alike.
#
# In order to provide replaceable clients (e.g. to switch between
# local and remote repositories) the module will provide various
# classes with the same interface (or with the same subset).
#
# Carried operations:
# - get basic info about repository
# - get a list of branches
# - get a list of commits
# - get info about a commit

import git
from gitdb.exc import BadObject
import time
import datetime
from github import Github, GithubException


class GitGithubClient(object):

	def __init__(self, username, project):
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

	def commits(self, branch, since = 0, to = datetime.datetime.now() + datetime.timedelta(hours=24)):
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
		for commit in self.repo.get_commits(sha = branch, since = since_dt, until = to):
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
		except (ValueError, KeyError, BadObject):
			raise KeyError("Commit %s not found" % commit)


class GitLocalClient(object):

	def __init__(self, repo_directory):
		self.repo = git.Repo(repo_directory)
		self.refs = {}

	def branches(self):
		"""Return a list of branches for given repository

		:return: [str]
		"""
		# get all remote branches
		refs = filter(lambda l: isinstance(l, git.RemoteReference), self.repo.references)
		# filter out HEAD branch
		refs = filter(lambda l: l.name != "origin/HEAD", refs)
		# filter out all branches not starting with 'origin/'
		refs = filter(lambda l: l.name.startswith("origin/"), refs)
		for ref in refs:
			self.refs[ref.name[7:]] = ref

		# remove 'origin/' prefix
		return map(lambda l: l.name[7:], refs)

	def _commitData(self, commit):
		"""Get data from a commit object

		:param commit: commit object
		:type  commit: git.objects.commit.Commit
		"""
		return {
			"hexsha": commit.hexsha,
			"adate": commit.authored_date,
			"cdate": commit.committed_date,
			"author": "%s <%s>" % (commit.author.name, commit.author.email),
			"message": commit.message
		}

	# http://stackoverflow.com/questions/9637838/convert-string-date-to-timestamp-in-python
	def commits(self, branch, since = 0, to = time.mktime((datetime.date.today() + datetime.timedelta(hours=24)).timetuple())):
		"""For given branch return a list of commits.
		Each commit contains basic information about itself.

		:param branch: git branch
		:type  branch: [str]{}
		:param since: minimal timestamp for commit's commit date
		:type  since: int
		:param to: maximal timestamp for commit's commit date
		:type  to: int
		"""
		# checkout the branch
		self.repo.create_head(branch, "refs/remotes/origin/%s" % branch)

		since_str = datetime.datetime.fromtimestamp(since).strftime('%Y-%m-%d %H:%M:%S')
		commits = {}
		for commit in self.repo.iter_commits(branch, since=since_str):
			# filter out all commits younger then to
			if commit.committed_date > to:
				continue

			commits[commit.hexsha] = self._commitData(commit)

		return commits

	def commit(self, commit):
		"""Get data for a given commit

		Raises KeyError if a commit is not found or not parsed.

		:param commit: repository commit
		:type  commit: string
		"""
		try:
			return self._commitData(self.repo.commit(commit))
		except (ValueError, KeyError, BadObject):
			raise KeyError("Commit %s not found" % commit)

if __name__ == "__main__":
	#client = GitLocalClient("/home/jchaloup/Packages/golang-github-abbot-go-http-auth/upstream/go-http-auth")
	client = GitLocalClient("/home/jchaloup/Packages/etcd/upstream/etcd")
	print(client.branches())
	#print ""
	#print len(client.commits("release-2.3").keys())
	print("")
	print(client.commit("5e6eb7e19d6385adfabb1f1caea03e732f9348ad"))
