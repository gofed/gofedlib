#
# Parser only parses, it does not retrieve missing commits or builds
#
# Currently supported:
# - upstream:[ipprefix|providerprefix][:commit]
# - user[:ipprefix]
# - [distribution|distro]:product[:version]:ipprefix
#

from __future__ import print_function

import re
from gofedlib.providers.providerbuilder import ProviderBuilder
from gofedlib.distribution.distributionnameparser import DistributionNameParser

class ProjectSignatureParser(object):

	def __init__(self):
		pass

	def parse(self, str):
		# upstream repository
		match = re.search(r"^upstream:([^:]+)(:(.*))?$", str)
		if match:
			provider = ProviderBuilder().buildUpstreamWithLocalMapping()
			signature = {
				"provider_type": "upstream_repository",
				"provider": provider.parse(match.group(1)),
				"commit": ""
			}
			if match.group(3):
				signature["commit"] = match.group(3)

			return signature

		# user directory
		match = re.search(r"^user(:(.*))(:(.*))?$", str)
		if match:
			signature = {
				"provider_type": "user_directory",
				"provider": {
					"provider": "user",
					"location": match.group(2)
				},
				"ipprefix": ""
			}
			if match.group(4):
				signature["ipprefix"] = match.group(2)

			return signature

		# distribution package
		match = re.match(r"^(distribution|distro):([^:]+)(:([^:]+))?:([^:]+)$", str)
		if match:
			version = "rawhide"
			if match.group(4):
				version = match.group(4)

			p = DistributionNameParser().parse("%s:%s" % (match.group(2), version))

			distribution = p.signature().json()

			signature = {
				"provider_type": "distribution_package",
				"provider": {
					"provider": "distribution",
					"product": distribution["product"],
					"version": distribution["version"]
				},
				"ipprefix": match.group(5)
			}

			return signature

		raise ValueError("No provider detected")

if __name__ == "__main__":
	p = ProjectSignatureParser()
	print(p.parse("upstream:github.com/coreos/etcd:434343"))
	print(p.parse("upstream:github.com/coreos/etcd"))
	print(p.parse("distro:Fedora:f23:gopkg.yaml/yaml.v1"))
