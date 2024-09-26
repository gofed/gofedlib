#!/bin/env python

import os
import subprocess
from setuptools import setup, find_packages
from distutils.command.install import install as DistutilsInstall


class GofedlibInstall(DistutilsInstall):

    def _compile_parsego(self):
        path = os.path.join("gofedlib", "go", "symbolsextractor")
        cmd = "go build -o %s %s" % (os.path.join(path,
                                                  "parseGo"), os.path.join(path, "parseGo.go"))

        process = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        retval = process.returncode

        if retval != 0:
            raise RuntimeError(stderr)

    def run(self):
        self._compile_parsego()
        return DistutilsInstall.run(self)


def get_requirements():
    with open('requirements.txt') as fd:
        return fd.read().splitlines()


def gofedlib_find_packages():
    packages = find_packages()
    # data files are often placed outside of package dir, we have to add them
    # manually
    additional = [
        'gofedlib.config',
        'gofedlib.docs',
        'gofedlib.distribution.clients.fakedata',
        'gofedlib.distribution.data',
        'gofedlib.go.apidiff.testdata',
        'gofedlib.go.importpath.data',
        'gofedlib.providers.data',
        'gofedlib.schemas'
    ]
    return packages + additional

setup(
    name='gofedlib',
    version='0.1.0',
    packages=gofedlib_find_packages(),
    scripts=['gofedlib-cli'],
    install_requires=get_requirements(),
    cmdclass={'install': GofedlibInstall},
    package_data={
        'gofedlib.config': ['lib.conf'],
        'gofedlib.docs': ['proposal.md', 'providers.md'],
        'gofedlib.distribution.clients.fakedata': ['data.json'],
        'gofedlib.distribution.clients.pkgdb': ['fakedata.json'],
        'gofedlib.distribution.data': ['ip2package_mapping.json'],
        'gofedlib.go.apidiff.testdata': ['api1.json', 'api2.json'],
        'gofedlib.go.importpath.data': ['known_prefixes.json', 'native_packages.json'],
        'gofedlib.go.symbolsextractor': ['parseGo.go', 'parseGo'],
        'gofedlib.logger': ['logger.yaml'],
        'gofedlib.providers.data': ['ip2pp_mapping.json'],
        'gofedlib.schemas': [
            'distribution_packages.json',
            'golang_native_imports.json',
            'import_path_to_package_name.json',
            'import_path_to_provider_prefix.json',
            'spec_model.json'
        ]
    },
    include_package_data=True,
    author='Jan Chaloupka',
    author_email='jchaloup@redhat.com',
    maintainer='Jan Chaloupka',
    maintainer_email='jchaloup@redhat.com',
    description='A set of python modules carrying operation related to Go source codes analysis used in Gofed',
    url='https://github.com/gofed/gofedlib',
    license='GPL',
    keywords='gofed golang API dependencies',
)
