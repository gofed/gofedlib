from importpathparserbuilder import ImportPathParserBuilder
from projectinfo import ProjectInfo

class ProjectInfoBuilder(object):

	def build(self):
		ipparser = ImportPathParserBuilder().buildWithLocalMapping()
		return ProjectInfo(ipparser)
