#
# Provide unique location of project snapshot in an ecosystem.
#
#

class ProjectResource(object):

	def __init__(self):
		pass

class RepositoryCommitResource(ProjectResource):

	def __init__(self, commit):
		ProjectResource.__init__(self)
		self._commit = commit

	def commit(self):
		return self._commit
	
class DistributionBuildResource(ProjectResource):

	def __init__(self, build):
		ProjectResource.__init__(self)
		self._build = build

	def build(self):
		return self._build

class ProjectResourceGenerator(object):

	def __init__(self):
		pass

	def repositoryCommit(self, commit):
		return RepositoryCommitResource(commit)

	def distributionBuild(self, build):
		return DistributionBuildResource(build)


class ProjectSignature(object):

	def __init__(self):
		self._resource = None
		self._provider = None

	def resource(self):
		raise NotImplementedError()

	def provider(self):
		raise NotImplementedError()

	def json(self):
		raise NotImplementedError()

	def __repr__(self):
		raise NotImplementedError()

class GithubRepositoryProjectSignature(ProjectSignature):

	def __init__(self, provider, commit):
		"""
		:param provider: github repository provider
		:type  provider: dict
		:param commit: repository commit
		:type  commit: ProjectResource
		"""
		ProjectSignature.__init__(self)
		self._provider = provider
		self._commit = commit

	def resource(self):
		return self._commit

	def provider(self):
		return self._provider

	def json(self):
		return {
			"provider": self._provider,
			"commit": self._commit
		}

	def __repr__(self):
		return str(self.json())

class BitbucketRepositoryProjectSignature(ProjectSignature):

	def __init__(self, provider, commit):
		"""
		:param provider: bitbucket repository provider
		:type  provider: dict
		:param commit: repository commit
		:type  commit: ProjectResource
		"""
		ProjectSignature.__init__(self)
		self._provider = provider
		self._commit = commit

	def resource(self):
		return self._commit

	def provider(self):
		return self._provider

	def json(self):
		return {
			"provider": self._provider,
			"commit": self._commit
		}

	def __repr__(self):
		return str(self.json())

class GooglecodeRepositoryProjectSignature(ProjectSignature):

	def __init__(self, provider, rev):
		"""
		:param provider: bitbucket repository provider
		:type  provider: dict
		:param rev: repository revision
		:type  rev: ProjectResource
		"""
		ProjectSignature.__init__(self)
		self._provider = provider
		self._rev = rev

	def resource(self):
		return self._rev

	def provider(self):
		return self._provider

	def json(self):
		return {
			"provider": self._provider,
			"rev": self._commit
		}

	def __repr__(self):
		return str(self.json())

class FedoraDistributionPackageProjectSignature(ProjectSignature):

	def __init__(self, provider, build):
		"""
		:param provider: distribution build provider
		:type  provider: dict
		:param build: distribution build
		:type  build: ProjectResource
		"""
		ProjectSignature.__init__(self)
		self._provider = provider
		self._build = build

	def provider(self):
		return self._provider

	def resource(self):
		return self._build

	def json(self):
		return {
			"provider": self._provider,
			"build": self._build
		}

	def __repr__(self):
		return str(self.json())

class ProjectSignatureGenerator(object):

	def __init__(self):
		pass

	def generate(self, resource_provider, resource):
		"""Generate project (snapshot) signature

		:param resource_provider: project provider
		:type  resource_provider: dict
		:param resource: project resource
		:type  resource: ProjectResource
		"""
		provider = resource_provider["provider"]
		if provider == "github":
			return self.generateGithubRepositorySignature(resource_provider, resource)
		if provider == "bitbucket":
			return self.generateBitbucketRepositorySignature(resource_provider, resource)
		if provider == "googlecode":
			return self.generateGooglecodeRepositorySignature(resource_provider, resource)
		if provider == "fedora":
			return self.generateFedoraDistributionPackageSignature(resource_provider, resource)

	def generateGithubRepositorySignature(self, provider, commit):
		return GithubRepositoryProjectSignature(provider, commit)

	def generateBitbucketRepositorySignature(self, provider, commit):
		return BitbucketRepositoryProjectSignature(provider, commit)

	def generateGooglecodeRepositorySignature(self, provider, commit):
		return GooglecodeRepositoryProjectSignature(provider, commit)

	def generateFedoraDistributionPackageSignature(self, provider, build):
		return FedoraDistributionPackageProjectSignature(provider, build)

