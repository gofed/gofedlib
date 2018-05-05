from .parserbuilder import ImportPathParserBuilder
from .decomposer import ImportPathsDecomposer

class ImportPathsDecomposerBuilder(object):

	def buildLocalDecomposer(self):
		ipparser = ImportPathParserBuilder().buildWithLocalMapping()
		return ImportPathsDecomposer(ipparser)

	def buildRemoteDecomposer(self):
		ipparser = ImportPathParserBuilder().buildWithRemoteMapping()
		return ImportPathsDecomposer(ipparser)
