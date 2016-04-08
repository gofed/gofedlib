#
# Build url for various resources:
# - upstream source code tarball
# - koji rpm
# - upstream repository clone url (github.com, bitbucket.org)
#

from gofed_lib.helpers import Build, Rpm

class UrlBuilder(object):

	def __init(self):
		pass

	def buildGithubSourceCodeTarball(self, username, project, commit):
		shortcommit = commit[:7]
		return "https://github.com/%s/%s/archive/%s/%s-%s.tar.gz" % (username, project, commit, project, shortcommit)

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

	def buildKojiRpm(self, product, build, rpm):
		if product == "Fedora":
			b = Build(build)
			r = Rpm(build, rpm)
			str_template = "https://kojipkgs.fedoraproject.org/packages/%s/%s/%s/%s/%s"
			return str_template % (b.name(), b.version(), b.release(), r.arch(), rpm)

		else:
			raise ValueError("Product '%s' not suppored" % product)

if __name__ == "__main__":
	b = UrlBuilder()
	print b.buildGithubSourceCodeTarball("coreos", "etcd", "4041bbe571432b6bc4bdd0a5408d55aba545b040")
	print b.buildGithubRepository("coreos", "etcd")
	print b.buildBitbucketRepository("ww", "goautoneg")
	print b.buildKojiRpm("Fedora", "etcd-2.3.1-1.fc25", "etcd-devel-2.3.1-1.fc25.noarch.rpm")
	print b.buildKojiRpm("Fedora", "etcd-2.3.1-1.fc25", "etcd-unit-test-2.3.1-1.fc25.armv7hl.rpm")
