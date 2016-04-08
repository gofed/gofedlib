import hglib
from hglib.util import b
import datetime
import time

class MercurialClient(object):

	def __init__(self, username, project):
		self.username = username
		self.project = project

	#def branches(self):


class MercurialLocalClient(object):

	def __init__(self, repo_directory):
		self.repo = hglib.open(repo_directory)
		self.refs = {}

	def branches(self):
		"""Return a list of branches for given repository

		:return: [str]
		"""
		# TODO(jchaloup): find out of all branches are listed (even remote)
		# if there is a concept of remote branch
		return map(lambda (b, r, n): b, self.repo.branches())

	def _commitData(self, changeset):
		"""Get data from a commit object

		:param changeset: tuple with changeset data
		:type  changeset: tuple
		"""
		(rev, node, tags, branch, author, desc, date) = changeset
		ts = int(time.mktime(date.timetuple()))
		return {
			"hexsha": node,
			"adate": ts,
			"cdate": ts,
			"author": author,
			"message": desc
		}

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
		commits = {}
		for changeset in self.repo.log(branch = "default"):
			commit = self._commitData(changeset)

			if commit["cdate"] < since:
				continue

			if commit["cdate"] > to:
				continue

			commits[commit["hexsha"]] = commit

		return commits

	def commit(self, commit):
		"""Get data for a given commit

		Raises KeyError if a commit is not found or not parsed.

		:param commit: repository commit
		:type  commit: string
		"""
		try:
			changesets = self.repo.log(revrange=commit)
		except error.CommandError:
			raise KeyError("Commit %s not found" % commit)

		return self._commitData(changesets[0])

if __name__ == "__main__":
	client = MercurialLocalClient("/home/jchaloup/Packages/golang-bitbucket-ww-goautoneg/upstream/goautoneg")
	#client.branches()
	#commits = client.commits("default", since = 1305929843)
	#for commit in commits: #, since=1313487608):
	#	print commits[commit]["cdate"]
	print client.commit("848b351341922ce39becda978778724d5b58dbca")
