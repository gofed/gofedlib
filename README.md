# lib
Gofed library is a set of python modules carrying operation related to Go source codes analysis.

Covered areas:
- go source code analysis (defined API, Go project dependencies, API diff)
- go project analysis (detection of dependency directories, documents, licenses)
- import path analysis (import path to distribution package mapping, import path to repository provider mapping, decomposition of imported paths based on known prefixes)
- dependency graph analysis (detection of cyclic dependencies)
- ecosystem scanning (new packages, new commits in upstream repositories, new builds in distribution builder)

## Examples

### Go source code analysis

There are three function to be called:

* project_packages - returns project's defined packages complying to [golang-project-packages](https://github.com/gofed/infra/blob/master/system/artefacts/schemas/golang-project-packages.json) JSON Schema
* api - returns project's exported API complying to [golang-project-exported-api](https://github.com/gofed/infra/blob/master/system/artefacts/schemas/golang-project-exported-api.json) JSON Schema
* apidiff - compare two API of a given project, returns comparison complying to [golang-projects-api-diff](https://github.com/gofed/infra/blob/master/system/artefacts/schemas/golang-projects-api-diff.json) JSON Schema

```python
# extract API and dependencies

from gofed_lib.gosymbolsextractor import api, project_packages
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
for package in etcd_packages["data"]["packages"]:
	print package
```
