#
# All communication with github.com, its remote positories
# or local ones will be carried through this module and alike.
#
# In order to provide replaceable clients (e.g. to switch between
# local and remote repositories) the module will provide various
# classes with the same interface (or with the same subset).
#
# Carried operations:
# - get basic info about repository
# - get a list of branches
# - get a list of commits
# - get info about a commit


if __name__ == "__main__":
	#client = GitLocalClient("/home/jchaloup/Packages/golang-github-abbot-go-http-auth/upstream/go-http-auth")
	client = GitLocalClient("/home/jchaloup/Packages/etcd/upstream/etcd")
	print(client.branches())
	#print ""
	#print len(client.commits("release-2.3").keys())
	print("")
	print(client.commit("5e6eb7e19d6385adfabb1f1caea03e732f9348ad"))
