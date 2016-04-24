# lib
Gofed library is a set of python modules carrying operation related to Go source codes analysis.

Covered areas:
- go source code analysis (defined API, Go project dependencies, API diff)
- go project analysis (detection of dependency directories, documents, licenses)
- import path analysis (import path to distribution package mapping, import path to repository provider mapping, decomposition of imported paths based on known prefixes)
- dependency graph analysis (detection of cyclic dependencies)
- ecosystem scanning (new packages, new commits in upstream repositories, new builds in distribution builder)

## Repository structure

* distribution (Koji, Bodhi, PkgDB, etc.)
* go (go symbols extractors, api diff, go project info, etc.)
* repositories (Git, Mercurial, Github.com, Bitbucket.com clients)
* urlbuilder (Github/Bitbucket source code tarball, rpm build, etc.)
* graphs (SCCs, subgraphs, graph transposition, etc.)

## How to install

There are two ways:

* clone the repository as gofed_lib directory under ``/usr/lib/python2.*/site-packages/`` (or ``/usr/lib/python3.*/site-packages/``)
* when running your code, set ``PYTHONPATH`` directory to point to gofed/lib's repository directory

## Examples

### Go source code analysis

There are three function to be called:

* project_packages - returns project's defined packages complying to ``data`` property's subset of [golang-project-packages](https://github.com/gofed/infra/blob/master/system/artefacts/schemas/golang-project-packages.json) JSON Schema
* api - returns project's exported API complying to ``packages`` property's [golang-project-exported-api](https://github.com/gofed/infra/blob/master/system/artefacts/schemas/golang-project-exported-api.json) JSON Schema
* apidiff - compare two API of a given project, returns comparison complying to ``data`` property's [golang-projects-api-diff](https://github.com/gofed/infra/blob/master/system/artefacts/schemas/golang-projects-api-diff.json) JSON Schema

```python
# extract API and dependencies

from gofed_lib.go.functions import api, project_packages
from gofed_lib.types import ExtractionError
import logging

source_code_directory = "~/Golang/etcd/etcd-5e6eb7e19d6385adfabb1f1caea03e732f9348ad"

try:
	etcd_api = api(source_code_directory)
	etcd_packages = project_packages(source_code_directory)
except ExtractionError as e:
	logging.error("Unable to extract %s: %s" % (source_code_directory, e))
	exit(1)

# print list of defined packages in etcd
print "Defined packages"
for package in etcd_packages["packages"]:
	print package
print ""

# print list of defined exported functions in etcd
print "Defined functions"
for package in etcd_api:
	print package["package"]
	for func in package["functions"]:
		print "\t%s" % func["name"]
print ""
```

```python
# API comparision

from gofed_lib.go.functions import api
from gofed_lib.go.functions import apidiff
from gofed_lib.types import ExtractionError
import logging

source_code_directory1 = "~/Golang/etcd/etcd-5e6eb7e19d6385adfabb1f1caea03e732f9348ad"
source_code_directory2 = "~/Golang/etcd/etcd-bc9ddf260115d2680191c46977ae72b837785472"

try:
	etcd_api1 = api(source_code_directory1)
except ExtractionError as e:
	logging.error("Unable to extract %s: %s" % (source_code_directory1, e))
	exit(1)

try:
	etcd_api2 = api(source_code_directory2)
except ExtractionError as e:
	logging.error("Unable to extract %s: %s" % (source_code_directory2, e))
	exit(1)

# get apidiff
try:
	api1_api2_diff = apidiff(etcd_api1, etcd_api2)
except ValueError as e:
	logging.error("Unable to compare API: %s" % e)
	exit(1)

# print updated symbols in API
for package in api1_api2_diff["updatedpackages"]:
        if "types" in package and "updated" in package["types"]:
                print "%s:" % package["package"]
                for change in package["types"]["updated"]:
                        print change
                print ""
```
