#
# Build url for various resources:
# - upstream source code tarball
# - koji rpm
# - upstream repository clone url (github.com, bitbucket.org)
#

from gofedlib.distribution.helpers import Build, Rpm

class UrlBuilder(object):

	def __init(self):
		pass

	def buildGithubSourceCodeTarball(self, username, project, commit):
		shortcommit = commit[:7]
		return "https://github.com/%s/%s/archive/%s/%s-%s.tar.gz" % (username, project, commit, project, shortcommit)

	def buildBitbucketSourceCodeTarball(self, username, project, commit):
		shortcommit = commit[:12]
		return "https://bitbucket.org/%s/%s/get/%s.tar.gz" % (username, project, shortcommit)

	def buildGithubRepository(self, username, project, protocol = "https"):
		if protocol == "https":
			return "https://github.com/%s/%s.git" % (username, project)
		else:
			raise ValueError("Protocol '%s' not supported" % protocol)

	def buildBitbucketRepository(self, username, project, protocol = "https"):
		if protocol == "https":
			return "https://bitbucket.org/%s/%s" % (username, project)
		else:
			raise ValueError("Protocol '%s' not supported" % protocol)

	def buildGithubProvider(self, provider):
		if provider["provider"] != "github":
			raise ValueError("Provider != github: %s" % provider["provider"])

		return "github.com/%s/%s" % (provider["username"], provider["project"])

	def buildBitbucketProvider(self, provider):
		if provider["provider"] != "bitbucket":
			raise ValueError("Provider != bitbucket: %s" % provider["provider"])

		return "bitbucket.org/%s/%s" % (provider["username"], provider["project"])

	def buildKojiRpm(self, product, build, rpm):
		if product == "Fedora":
			b = Build(build)
			r = Rpm(build, rpm)
			str_template = "https://kojipkgs.fedoraproject.org/packages/%s/%s/%s/%s/%s"
			return str_template % (b.name(), b.version(), b.release(), r.arch(), rpm)

		else:
			raise ValueError("Product '%s' not suppored" % product)

