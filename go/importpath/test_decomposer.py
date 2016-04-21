import unittest
from .decomposerbuilder import ImportPathsDecomposerBuilder

class ImportPathsDecomposerTest(unittest.TestCase):

	def test(self):

		paths = [
			"github.com/akrennmair/gopcap",
			"github.com/bgentry/speakeasy",
			"github.com/boltdb/bolt",
			"github.com/cheggaaa/pb",
			"github.com/codegangsta/cli",
			"github.com/coreos/go-semver/semver",
			"github.com/coreos/go-systemd/daemon",
			"github.com/coreos/go-systemd/util",
			"github.com/coreos/pkg/capnslog",
			"github.com/gogo/protobuf/proto",
			"github.com/google/btree",
			"github.com/jonboulle/clockwork",
			"github.com/olekukonko/tablewriter",
			"github.com/prometheus/client_golang/prometheus",
			"github.com/prometheus/procfs",
			"github.com/spacejam/loghisto",
			"github.com/spf13/cobra",
			"github.com/spf13/pflag",
			"github.com/ugorji/go/codec",
			"github.com/xiang90/probing",
			"golang.org/x/crypto/bcrypt",
			"golang.org/x/net/context",
			"google.golang.org/grpc",
			"google.golang.org/grpc/codes",
			"google.golang.org/grpc/credentials",
			"google.golang.org/grpc/grpclog",
			"fmt",
			"net/http",
			"net/url",
			"strings"
		]

		d = ImportPathsDecomposerBuilder().buildLocalDecomposer()
		d.decompose(paths)

		expected_classes = set([
			"github.com/akrennmair/gopcap",
			"github.com/bgentry/speakeasy",
			"github.com/boltdb/bolt",
			"github.com/cheggaaa/pb",
			"github.com/codegangsta/cli",
			"github.com/coreos/go-semver",
			"github.com/coreos/go-systemd",
			"github.com/coreos/pkg",
			"github.com/gogo/protobuf",
			"github.com/google/btree",
			"github.com/jonboulle/clockwork",
			"github.com/olekukonko/tablewriter",
			"github.com/prometheus/client_golang",
			"github.com/prometheus/procfs",
			"github.com/spacejam/loghisto",
			"github.com/spf13/cobra",
			"github.com/spf13/pflag",
			"github.com/ugorji/go",
			"github.com/xiang90/probing",
			"golang.org/x/crypto",
			"golang.org/x/net",
			"google.golang.org/grpc",
			"Native"
		])

		# classes match
		self.assertEqual(set(d.classes().keys()), expected_classes)

		

