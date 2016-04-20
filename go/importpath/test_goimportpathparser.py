import unittest
import json
import os
from goimportpathparser import GoImportPathParser

class GoImportPathParserTest(unittest.TestCase):

	def test(self):

		paths = [{
			"path": "github.com/coreos/etcd/pkg/netutil",
			"prefix": "github.com/coreos/etcd",
			"package": "pkg/netutil",
			"native": False
		},{
			"path": "github.com/coreos/etcd/pkg/types",
			"prefix": "github.com/coreos/etcd",
			"package": "pkg/types",
			"native": False
		},{
			"path": "github.com/coreos/go-systemd/daemon",
			"prefix": "github.com/coreos/go-systemd",
			"package": "daemon",
			"native": False
		},{
			"path": "github.com/xiang90/probing",
			"prefix": "github.com/xiang90/probing",
			"package": "",
			"native": False
		},{
			"path": "golang.org/x/crypto/bcrypt",
			"prefix": "golang.org/x/crypto",
			"package": "bcrypt",
			"native": False
		},{
			"path": "golang.org/x/net/context",
			"prefix": "golang.org/x/net",
			"package": "context",
			"native": False
		},{
			"path": "google.golang.org/grpc",
			"prefix": "google.golang.org/grpc",
			"package": "",
			"native": False
		},{
			"path": "google.golang.org/grpc/credentials",
			"prefix": "google.golang.org/grpc",
			"package": "credentials",
			"native": False
		},{
			"path": "code.google.com/p/goauth2/compute/serviceaccount",
			"prefix": "code.google.com/p/goauth2",
			"package": "compute/serviceaccount",
			"native": False
		},{
			"path": "code.google.com/p/google-api-go-client/googleapi",
			"prefix": "code.google.com/p/google-api-go-client",
			"package": "googleapi",
			"native": False
		},{
			"path": "bitbucket.org/kardianos/osext",
			"prefix": "bitbucket.org/kardianos/osext",
			"package": "",
			"native": False
		},{
			"path": "gopkg.in/gcfg.v1/scanner",
			"prefix": "gopkg.in/gcfg.v1",
			"package": "scanner",
			"native": False
		},{
			"path": "gopkg.in/v1/gcfg/scanner",
			"prefix": "gopkg.in/v1/gcfg",
			"package": "scanner",
			"native": False
		},{
			"path": "gopkg.in/fsnotify.v0",
			"prefix": "gopkg.in/fsnotify.v0",
			"package": "",
			"native": False
		},{
			"path": "bazil.org/fuse/aaa",
			"prefix": "bazil.org/fuse",
			"package": "aaa",
			"native": False
		},{
			"path": "camlistore.org/aaa",
			"prefix": "camlistore.org",
			"package": "aaa",
			"native": False
		},{
			"path": "collectd.org/aaa",
			"prefix": "collectd.org",
			"package": "aaa",
			"native": False
		},{
			"path": "gopkg.in/fatih/pool.v2/aaa",
			"prefix": "gopkg.in/fatih/pool.v2",
			"package": "aaa",
			"native": False
		},{
			"path": "gopkg.in/olivere/elastic.v2/aaa",
			"prefix": "gopkg.in/olivere/elastic.v2",
			"package": "aaa",
			"native": False
		},{
			"path": "k8s.io/heapster/aaa",
			"prefix": "k8s.io/heapster",
			"package": "aaa",
			"native": False
		},{
			"path": "k8s.io/kubernetes/aaa",
			"prefix": "k8s.io/kubernetes",
			"package": "aaa",
			"native": False
		},{
			"path": "gopkg.in/natefinch/lumberjack.v1/aaa",
			"prefix": "gopkg.in/natefinch/lumberjack.v1",
			"package": "aaa",
			"native": False
		},{
			"path": "launchpad.net/gocheck/check",
			"prefix": "launchpad.net/gocheck",
			"package": "check",
			"native": False
		},{
			"path": "speter.net/go/exp/math/dec/inf/aaa",
			"prefix": "speter.net/go/exp/math/dec/inf",
			"package": "aaa",
			"native": False
		}]

		script_dir = os.path.dirname(os.path.realpath(__file__))
		prefixes_file = os.path.join(script_dir, "data/known_prefixes.json")
		packages_file = os.path.join(script_dir, "data/native_packages.json")

		with open(prefixes_file, "r") as f:
			regexs = json.load(f)

		with open(packages_file, "r") as f:
			native = json.load(f)

		p = GoImportPathParser(regexs, native)

		for path in paths:
			p.parse(path["path"])
			self.assertEqual(path["native"], p.isNative())
			if not path["native"]:
				self.assertEqual(path["prefix"], p.prefix())
				self.assertEqual(path["package"], p.package())

