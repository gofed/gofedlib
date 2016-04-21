#
# Capture the current state of a project. Common datas so far:
# - commit (commit of the project or commit packaged/captured in distribution/other storage medium)
# - provider signature (repository, distribution, collection, ...)
#
# Later, possibly:
# - other numbers (trend, healthiness, ...)
#
# The snapshot is a product of ProjectCapturer.
# 
#
#
class ProjectSnapshotCapturer(object)

	def capture(self, provider):
		"""Generate snapshot's signature
		"""
		raise NotImplementedError()

	def signature(self):
		raise NotImplementedError()
