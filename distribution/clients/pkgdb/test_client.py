import unittest
from fakeclient import FakePkgDBClient
from client import PkgDBClient
import json
from lib.utils import getScriptDir

class PkgDBClienTest(unittest.TestCase):

	def test(self):

		client = FakePkgDBClient()
		self.assertFalse(client.packageExists("test"))
		self.assertNotEqual(client.getGolangPackages(), {})
		self.assertNotEqual(client.getCollections(), {})

