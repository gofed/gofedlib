import git
from gitdb.exc import BadObject
import time
import datetime

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
	def commits(self, branch, since = 0, to = int(time.time()) + 86400):
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
