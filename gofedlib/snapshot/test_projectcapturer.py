import unittest
from .capturer import ProjectCapturer
from .projectgithubrepositorycapturer import ProjectGithubRepositoryCapturer
from .projectbitbucketrepositorycapturer import ProjectBitbucketRepositoryCapturer

class ProjectCapturerTest(unittest.TestCase):

	def test(self):

		fake_commit = "69bc0f76bc04078baafd88e243658730d67b5249"
		class FakeClient(object):

			def latestCommit(self):
				return fake_commit

		fake_client = FakeClient()

		provider = {
			"provider": "github",
			"username": "user",
			"project": "test"
		}
		expected = {
			'commit': fake_commit,
			'resource_url': 'https://github.com/user/test/archive/%s/test-%s.tar.gz' % (fake_commit, fake_commit[:7]),
			'provider': provider
		}

		self.assertEqual(
			ProjectGithubRepositoryCapturer(provider, fake_client).capture().signature(),
			expected
		)

		provider = {
			"provider": "bitbucket",
			"username": "user",
			"project": "test"
		}
		expected = {
			'commit': fake_commit,
			"resource_url": "https://bitbucket.org/user/test/get/%s.tar.gz" % (fake_commit[:12]),
			'provider': provider
		}

		self.assertEqual(
			ProjectBitbucketRepositoryCapturer(provider, fake_client).capture().signature(),
			expected
		)

