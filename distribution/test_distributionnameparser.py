import unittest
from .distributionnameparser import DistributionNameParser

class DistributionNameParserTest(unittest.TestCase):

	def test(self):
		parser = DistributionNameParser()

		names = []
		names.append("Fedora 	22")
		names.append("F22")
		names.append("Fedora:f22")
		names.append("Fedora:22")

		expected = {"product": "Fedora", "version": "22"}

		for name in names:
			actual = parser.parse(name).getSignature()
			self.assertEqual(expected, actual)
