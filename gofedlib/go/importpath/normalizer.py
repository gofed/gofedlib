# Some import paths does not have to correspond exactly to imported project.
# E.g. github.com/coreos/etcd/Godeps/_workspace/src/github.com/boltdb/bolt
# is actually github.com/boltdb/bolt.
#
# I have encountered with this behaviour only for Godeps/_workspace/src case.
#
# Aim of the normalizer is to replace all such occurrences with the actual
# project package
#

class ImportPathNormalizer(object):

	def __init__(self):
		pass

	def normalize(self, import_path):
		for pattern in ["Godeps/_workspace/src"]:
			index = import_path.find(pattern)
			if index != -1:
				return import_path[index + len(pattern) + 1:]

		return import_path
		
