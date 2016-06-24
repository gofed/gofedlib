#
# Mostly just to check the extractor works and no modules are missing at this point
# TODO(jchaloup): validate the data based on modified JSON Schema from gofed/infra
#

import unittest
from lib.utils import getScriptDir
import os
from .extractor import GoSymbolsExtractor

class GoSymbolsExtractorTest(unittest.TestCase):

	def test(self):

		source_code_directory = "%s/testdata/example" % getScriptDir(__file__)

		e = GoSymbolsExtractor(source_code_directory).extract()

		# TODO(jchaloup): validate the schema
		self.assertNotEquals(e.packages(), {'main': [], 'tests': [], 'dependencies': [], 'packages': []})
		self.assertNotEquals(e.exportedApi(), [])
