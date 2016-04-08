#
# Call simple functions without knowing who actually provides the url construction algorithm
#
from .urlbuilder import UrlBuilder

def github_source_code_tarball_url(username, project, commit):
	return UrlBuilder().buildGithubSourceCodeTarball(username, project, commit)

def github_repository_url(username, project):
	return UrlBuilder().buildGithubRepository(username, project)

def bitbucket_repository_url(username, project):
	return UrlBuilder().buildBitbucketRepository(username, project)

def koji_rpm_url(product, build, rpm):
	return UrlBuilder().buildKojiRpm(product, build, rpm)

if __name__ == "__main__":
	print github_source_code_tarball_url("coreos", "etcd", "4041bbe571432b6bc4bdd0a5408d55aba545b040")
	print github_repository_url("coreos", "etcd")
	print bitbucket_repository_url("ww", "goautoneg")
	print koji_rpm_url("Fedora", "etcd-2.3.1-1.fc25", "etcd-devel-2.3.1-1.fc25.noarch.rpm")
