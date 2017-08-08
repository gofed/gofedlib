from .githubclient import GithubClient
from .bitbucketclient import BitbucketClient
from .gitlocalclient import GitLocalClient
from .mercuriallocalclient import MercurialLocalClient
import os

class RepositoryClientBuilder(object):

	def buildWithRemoteClient(self, repo_info, lazy=True):

		if repo_info['provider'] == 'github':
			return GithubClient(repo_info['username'], repo_info['project'], lazy)
		if repo_info['provider'] == 'bitbucket':
			return BitbucketClient(repo_info['username'], repo_info['project'])

		raise ValueError("Unsupported provider: %s" % repo_info['provider'])

	def buildWithLocalClient(self, repo_info, repository_directory):

		if not os.path.isdir(repository_directory):
			raise ValueError('Directory not found: %s' % repository_directory)

		if os.path.exists("%s/.git" % repository_directory):
			return GitLocalClient(repository_directory, repo_info)

		if os.path.exists("%s/.hg" % repository_directory):
			return MercurialLocalClient(repository_directory)

		raise ValueError("Unsupported VCS repository in directory: %s" % repository_directory)
