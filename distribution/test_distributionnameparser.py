import unittest
from distributionnameparser import DistributionNameParser
import logging

logging.basicConfig(level=logging.DEBUG)

class DistributionNameParserTest(unittest.TestCase):

	def test(self):
		print ""

		parser = DistributionNameParser()

		names = []
		names.append("Fedora 	22")
		names.append("F22")
		names.append("Fedora:f22")
		names.append("Fedora:22")

		expected = {"product": "Fedora", "version": "22"}

		for name in names:
			logging.debug("Parsing \"%s\"" % name)
			actual = parser.parse(name).getSignature()
			self.assertEqual(expected, actual)
