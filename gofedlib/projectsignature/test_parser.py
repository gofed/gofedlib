import unittest
from .parser import ProjectSignatureParser

class ProjectSignatureParserTest(unittest.TestCase):

	def test(self):

		strs = [{
			"str": "upstream:github.com/coreos/etcd:434343",
			"expected": {
				"provider_type": "upstream_repository",
				"provider": {
					'username': 'coreos',
					'project': 'etcd',
					'provider': 'github'
				},
				'commit': '434343'
			}
		},{
			"str": "upstream:github.com/coreos/etcd",
			"expected": {
				"provider_type": "upstream_repository",
				"provider": {
					'username': 'coreos',
					'project': 'etcd',
					'provider': 'github'
				},
				"commit": ""
			}
		},{
			"str": "distro:Fedora:f23:gopkg.yaml/yaml.v1",
			"expected": {
				"provider_type": "distribution_package",
				"provider": {
					'product': 'Fedora',
					'version': '23',
					'provider': 'distribution'
				},
				'ipprefix': 'gopkg.yaml/yaml.v1'
			}
		}]

		p = ProjectSignatureParser()
		for str in strs:
			self.assertEqual(p.parse(str["str"]), str["expected"])

