#
# Mostly just to check the apidiff works and no modules are missing at this point
# TODO(jchaloup): validate the data based on modified JSON Schema from gofed/infra
#

import unittest
import json
from lib.utils import getScriptDir
from .apidiff import GoApiDiff

class ApiDiffTest(unittest.TestCase):

	def test(self):

		api1_path = "%s/testdata/api1.json" % getScriptDir(__file__)
		api2_path = "%s/testdata/api2.json" % getScriptDir(__file__)

		with open(api1_path, "r") as f:
			api1 = json.load(f)

		with open(api2_path, "r") as f:
			api2 = json.load(f)

		d = GoApiDiff(api1, api2).runDiff()

		# TODO(jchaloup): validate the api diff
		self.assertNotEqual(d.apiDiff(), {})
