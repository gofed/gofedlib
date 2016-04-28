import unittest
from fakeclient import FakeKojiClient
import json
from lib.utils import getScriptDir

class KojiClienTest(unittest.TestCase):

	def test(self):

		client = FakeKojiClient()
		self.assertNotEqual(client.getLatestRPMS("rawhide", "golang-github-evanphx-json-patch"), {})
		self.assertNotEqual(client.getPackageBuilds("rawhide", "gofed"), {})
