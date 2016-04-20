import unittest
import json
from upstreamprovider import UpstreamProvider

class UpstreamProviderTest(unittest.TestCase):

	def test(self):

		prefixes = [{
			"prefix": "github.com/coreos/etcd",
			"signature": {"provider": "github", "username": "coreos", "project": "etcd"}
		},{
			"prefix": "github.com/coreos/go-systemd",
			"signature": {"provider": "github", "username": "coreos", "project": "go-systemd"}
		},{
			"prefix": "github.com/xiang90/probing",
			"signature": {"provider": "github", "username": "xiang90", "project": "probing"}
		},{
			"prefix": "golang.org/x/crypto",
			"signature": {"provider": "golangorg", "username": "", "project": "crypto"}
		},{
			"prefix": "golang.org/x/net",
			"signature": {"provider": "golangorg", "username": "", "project": "net"}
		},{
			"prefix": "google.golang.org/grpc",
			"signature": {"provider": "googlegolangorg", "username": "", "project": "grpc"}
		},{
			"prefix": "code.google.com/p/goauth2",
			"signature": {"provider": "googlecode", "username": "", "project": "goauth2"}
		},{
			"prefix": "code.google.com/p/google-api-go-client",
			"signature": {"provider": "googlecode", "username": "", "project": "google-api-go-client"}
		},{
			"prefix": "bitbucket.org/kardianos/osext",
			"signature": {"provider": "bitbucket", "username": "kardianos", "project": "osext"}
		},{
			"prefix": "gopkg.in/gcfg.v1",
			"signature": {"provider": "gopkg", "username": "", "project": "gcfg", "version": "v1"}
		},{
			"prefix": "gopkg.in/v1/gcfg",
			"signature": {"provider": "gopkg", "username": "", "project": "gcfg", "version": "v1"}
		},{
			"prefix": "gopkg.in/fsnotify.v0",
			"signature": {"provider": "gopkg", "username": "", "project": "fsnotify", "version": "v0"}
		},{
			"prefix": "gopkg.in/fatih/pool.v2",
			"signature": {"provider": "gopkg", "username": "fatih", "project": "pool", "version": "v2"}
		},{
			"prefix": "gopkg.in/olivere/elastic.v2",
			"signature": {"provider": "gopkg", "username": "olivere", "project": "elastic", "version": "v2"}
		},{
			"prefix": "gopkg.in/natefinch/lumberjack.v1",
			"signature": {"provider": "gopkg", "username": "natefinch", "project": "lumberjack", "version": "v1"}
		}]

		with open("import_path_to_provider_prefix_mapping.json", "r") as f:
			ip2pp = json.load(f)

		p = UpstreamProvider([])

		for prefix in prefixes:
			p.parse(prefix["prefix"])

			self.assertEqual(p.prefix(), prefix["prefix"])
			self.assertEqual(p.signature(), prefix["signature"])
