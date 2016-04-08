from .repo.githubclient import GithubClient
from .repo.bitbucketclient import BitbucketClient
from .repo.gitlocalclient import GitLocalClient
from .repo.mercuriallocalclient import MercurialLocalClient
import os


class RepositoryClientBuilder(object):

	def buildWithRemoteClient(self, repo_info):
		if repo_info['provider'] == 'github':
			return GithubClient(repo_info['username'], repo_info['project'])
		if repo_info['provider'] == 'bitbucket':
			return BitbucketClient(repo_info['username'], repo_info['project'])
		raise ValueError("Unsupported provider: %s" % repo_info['provider'])

	def buildWithLocalClient(self, repo_info):
		if not os.path.isdir(repo_info['repository_directory']):
			raise ValueError('Directory not found: ' + repo_info['repository_directory'])

		if os.path.exists(repo_info['repository_directory'] + '/.git'):
			return GitLocalClient(repo_info['repository_directory'])
		if os.path.exists(repo_info['repository_directory'] + '/.hg'):
			return MercurialLocalClient(repo_info['repository_directory'])
		raise ValueError("Unsupported VCS repository in directory: %s" % repo_info['repository_directory'])
