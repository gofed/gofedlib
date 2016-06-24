import unittest
from .builder import UrlBuilder

class UrlBuilderTest(unittest.TestCase):

	def test(self):

		b = UrlBuilder()

		self.assertEqual(
			b.buildGithubSourceCodeTarball(
				"coreos",
				"etcd",
				"4041bbe571432b6bc4bdd0a5408d55aba545b040"
			),
			"https://github.com/coreos/etcd/archive/4041bbe571432b6bc4bdd0a5408d55aba545b040/etcd-4041bbe.tar.gz"
		)

		self.assertEqual(
			b.buildBitbucketSourceCodeTarball(
				"ww",
				"goautoneg",
				"75cd24fc2f2c2a2088577d12123ddee5f54e0675"
			),
			"https://bitbucket.org/ww/goautoneg/get/75cd24fc2f2c.tar.gz"
		)

		self.assertEqual(
			b.buildGithubRepository("coreos", "etcd"),
			"https://github.com/coreos/etcd.git"
		)

		self.assertEqual(
			b.buildBitbucketRepository("ww", "goautoneg"),
			"https://bitbucket.org/ww/goautoneg"
		)

		self.assertEqual(
			b.buildKojiRpm(
				"Fedora",
				"etcd-2.3.1-1.fc25",
				"etcd-devel-2.3.1-1.fc25.noarch.rpm"
			),
			"https://kojipkgs.fedoraproject.org/packages/etcd/2.3.1/1.fc25/noarch/etcd-devel-2.3.1-1.fc25.noarch.rpm"
		)

		self.assertEqual(
			b.buildKojiRpm(
				"Fedora",
				"etcd-2.3.1-1.fc25",
				"etcd-unit-test-2.3.1-1.fc25.armv7hl.rpm"
			),
			"https://kojipkgs.fedoraproject.org/packages/etcd/2.3.1/1.fc25/armv7hl/etcd-unit-test-2.3.1-1.fc25.armv7hl.rpm"
		)

		self.assertEqual(
			b.buildGithubProvider({
				"provider": "github",
				"username": "coreos",
				"project": "etcd"
			}),
			"github.com/coreos/etcd"
		)

		self.assertEqual(
			b.buildBitbucketProvider({
				"provider": "bitbucket",
				"username": "ww",
				"project": "goautoneg"
			}),
			"bitbucket.org/ww/goautoneg"
		)

