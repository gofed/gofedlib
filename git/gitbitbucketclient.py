import datetime
import json
import requests


class GitBitbucketClient(object):

	def __init__(self, username, project):
		self.reponame = username + '/' + project

	def branches(self):
		"""Return a list of branches for given repository

		:return: [str]
		"""
		req_message = 'https://api.bitbucket.org/1.0/repositories/' + self.reponame + '/branches'
		response = requests.get(req_message)
		if response.status_code != 200:
			raise KeyError('Failed to get repository information: %s:%s'
						   % (str(response.status_code), self.reponame))
		response_data = json.loads(response.text)


	def _commitData(self, commit):
		"""Get data from a commit object

		:param commit: commit object
		:type  commit: git.objects.commit.Commit
		"""
		pass

	def commits(self, branch, since = 0, to = datetime.datetime.now() + datetime.timedelta(hours=24)):
		"""For given branch return a list of commits.
		Each commit contains basic information about itself.

		:param branch: git branch
		:type  branch: [str]{}
		:param since: minimal timestamp for commit's commit date
		:type  since: int
		:param to: maximal timestamp for commit's commit date
		:type  to: int
		"""
		pass

	def commit(self, commit):
		"""Get data for a given commit

		Raises KeyError if a commit is not found or not parsed.

		:param commit: repository commit
		:type  commit: string
		"""
		pass