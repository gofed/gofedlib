import unittest
from .packagenamegeneratorbuilder import PackageNameGeneratorBuilder
from .packagenamegenerator import PackageNameGenerator

class PackageNameGeneratorTest(unittest.TestCase):

	def test(self):

		projects = [{
			"project": "gopkg.in/check.v1",
			"name": "golang-gopkg-check",
			"mname": "golang-gopkg-check"
		},{
			"project": "github.com/coreos/etcd",
			"name": "golang-github-coreos-etcd",
			"mname": "etcd"
		},{
			"project": "gopkg.in/v1/check",
			"name": "golang-gopkg-check",
			"mname": "golang-gopkg-check"
		},{
			"project": "gopkg.in/natefinch/lumberjack.v1",
			"name": "golang-gopkg-natefinch-lumberjack",
			"mname": "golang-gopkg-natefinch-lumberjack"
		},{
			"project": "code.google.com/p/google-api-go-client",
			"name": "golang-googlecode-google-api-go-client",
			"mname": "golang-googlecode-google-api-client"
		},{
			"project": "golang.org/x/oauth2",
			"name": "golang-golangorg-oauth2",
			"mname": "golang-googlecode-goauth2"
		},{
			"project": "camlistore.org",
			"name": "golang-camlistore",
			"mname": "camlistore"
		},{
			"project": "bitbucket.org/ww/goautoneg",
			"name": "golang-bitbucket-ww-goautoneg",
			"mname": "golang-bitbucket-ww-goautoneg"
		},{
			"project": "k8s.io/heapster",
			"name": "golang-k8s-heapster",
			"mname": "golang-github-kubernetes-heapster"
		}]

		g = PackageNameGenerator()
		for project in projects:
			self.assertEqual(g.generate(project["project"]).name(), project["name"])

		g = PackageNameGeneratorBuilder().buildWithLocalMapping()
		for project in projects:
			self.assertEqual(g.generate(project["project"]).name(), project["mname"])

