from fedora.client import BodhiClient as BClient
from fedora.client.bodhi import BodhiClientException

# https://github.com/fedora-infra/bodhi/blob/develop/tools/python-fedora-api-test.py
# https://github.com/fedora-infra/python-fedora/blob/develop/fedora/client/bodhi.py

import logging

class BodhiClient(object):

	def __init__(self, username, password):
		self.bodhi = BClient(username=username, password=password)

	def createUpdate(self, builds, notes, bugs, type="enhancement"):
		try:
			result = self.bodhi.save(builds=builds, type=type, notes=notes, bugs=bugs)
		except BodhiClientException as e:
			logging.error(e)
			return False

		return True

	def createNewPackageUpdate(self, builds, notes, bugs):
		return self.createUpdate(builds, notes, bugs, type="newpackage")

# Example
# bodhi.save(builds="golang-googlecode-uuid-0-0.8.gitca53cad.fc24", type="enhancement", notes="Update", bugs="1250523", edited="golang-googlecode-uuid-0-0.8.gitca53cad.fc24")
#
#
#
