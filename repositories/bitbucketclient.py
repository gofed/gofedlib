# https://confluence.atlassian.com/bitbucket/commits-or-commit-resource-389775478.html

import datetime
import time
import json
import requests

class BitbucketClient(object):

	def __init__(self, project, repository):
		self.reponame = project + '/' + repository

	def _bitbucketAPIRequest(self, req_message):
		if not req_message:
			raise ValueError ('request message empty')
		response = requests.get(req_message)
		if response.status_code != 200:
			raise KeyError('Failed to get repository information: %s:%s'
						   % (str(response.status_code), self.reponame))
		return json.loads(response.text)

	def branches(self):
		"""Return a list of branches for given repository

		:return: [str]
		"""
		req_message = 'https://api.bitbucket.org/1.0/repositories/' + self.reponame + '/branches'
		response_data = self._bitbucketAPIRequest(req_message)
		return response_data.keys()

	def _commitData(self, commit):
		"""Get data from a commit object

		:param commit: commit object
		:type  commit: git.objects.commit.Commit
		"""
		return {
			"hexsha": commit['hash'],
			"adate": time.mktime(time.strptime(commit['date'][:19], '%Y-%m-%dT%H:%M:%S')),
			"cdate": time.mktime(time.strptime(commit['date'][:19], '%Y-%m-%dT%H:%M:%S')),
			"author": commit['author']['raw'],
			"message": commit['message']
		}

	def commits(self, branch, since=0, to=int(time.time()) + 86400):
		"""For given branch return a list of commits.
		Each commit contains basic information about itself.

		:param branch: git branch
		:type  branch: [str]{}
		:param since: minimal timestamp for commit's commit date
		:type  since: int
		:param to: maximal timestamp for commit's commit date
		:type  to: int
		"""

		since_str = datetime.datetime.fromtimestamp(since).strftime('%Y-%m-%d')
		to_str = datetime.datetime.fromtimestamp(to).strftime('%Y-%m-%d')
		commits = {}
		req_message = 'https://api.bitbucket.org/2.0/repositories/' + self.reponame + \
					  '/commits/' + branch

		loop_continue = True
		while loop_continue:
			response_data = self._bitbucketAPIRequest(req_message)
			for commit in response_data['values']:
				if commit['date'] < since_str:
					loop_continue = False
					break
				elif commit['date'] > to_str:
					continue
				else:
					commits[commit['hash']] = self._commitData(commit)

			if 'next' not in response_data:
				break
			req_message = response_data['next']
		return commits

	def commit(self, commit):
		"""Get data for a given commit

		Raises KeyError if a commit is not found or not parsed.

		:param commit: repository commit
		:type  commit: string
		"""
		req_message = 'https://api.bitbucket.org/2.0/repositories/atlassian/aui/commit/' + commit
		response_data = self._bitbucketAPIRequest(req_message)
		try:
			return self._commitData(response_data)
		except (ValueError, KeyError):
			raise KeyError("Commit %s not found" % commit)

	def latestCommit(self):
		req_message = "https://api.bitbucket.org/2.0/repositories/%s/commits/default" % self.reponame

		response_data = self._bitbucketAPIRequest(req_message)
		for commit in response_data['values']:
			return self._commitData(commit)

		raise KeyError("Latest commit not found")

