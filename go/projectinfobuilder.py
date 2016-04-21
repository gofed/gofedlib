from .importpath.parserbuilder import ImportPathParserBuilder
from .projectinfo import ProjectInfo

class ProjectInfoBuilder(object):

	def build(self):
		ipparser = ImportPathParserBuilder().buildWithLocalMapping()
		return ProjectInfo(ipparser)
