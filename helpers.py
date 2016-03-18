class NVR(object):

	def __init__(self, name):
		self._name = name
		self._parse()

	def _parse(self):
		# get n,v,r from build
		parts = self._name.split("-")
		if len(parts) < 3:
			raise ValueError("Invalid nvr: %s" % self._name)

		self._release = parts[-1]
		self._version = parts[-2]
		self._name = "-".join(parts[:-2])

		parts = self._release.split(".")
		if len(parts) < 2:
			raise ValueError("Invalid nvr: %s" % self._name)

		# e.g. etcd-2.2.4-2.fc24
		self._tag = parts[-1]

	def name(self):
		return self._name

	def version(self):
		return self._version

	def release(self):
		return self._release

	def tag(self):
		return self._tag


class Build(object):

	def __init__(self, build):
		self.build = build
		self.nvr = NVR(build)

	def srpm(self):
		"""Construct srpm from build"""
		return "%s.src.rpm" % self.build

	def name(self):
		return self.nvr.name()

	def version(self):
		return self.nvr.version()

	def release(self):
		return self.nvr.release()

	def tag(self):
		return self.nvr.tag()

class Rpm(object):

	def __init__(self, build, rpm):
		self.rpm = rpm
		self.build = build
		self._parse()

	def _parse(self):
		r_nvr = NVR(self.rpm)
		self.r_name = r_nvr.name()

		# get architecture
		parts = self.rpm.split(".")
		if len(parts) < 3:
			raise ValueError("Invalid rpm nvr.arch.rpm: %s" % self.rpm)

		if parts[-1] != "rpm":
			raise ValueError("Invalid rpm nvr.arch.rpm: %s" % self.rpm)

		self._arch = parts[-2]

		# get nvr
		b_nvr = NVR(self.build)
		self.b_release = b_nvr.release()
		self.b_version = b_nvr.release()
		self.b_name = b_nvr.name()

	def name(self):
		return self.r_name

	def arch(self):
		return self._arch

	def download_url(self):
		# construct download url
		# https://kojipkgs.fedoraproject.org//packages/etcd/2.2.4/2.fc24/noarch/etcd-devel-2.2.4-2.fc24.noarch.rpm
		# https://kojipkgs.fedoraproject.org//packages/etcd/2.2.4/2.fc24/x86_64/etcd-unit-test-2.2.4-2.fc24.x86_64.rpm
		# https://kojipkgs.fedoraproject.org//packages/etcd/2.2.4/2.fc24/src/etcd-2.2.4-2.fc24.src.rpm
		return "https://kojipkgs.fedoraproject.org/packages/%s/%s/%s/%s/%s" % (self.b_name, self.b_version, self.b_release, self._arch, self.rpm)
