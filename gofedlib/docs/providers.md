# Go project providers (DRAFT)

Entire Go ecosystem consists of Go projects.
Each project is provided by at least one system (e.g. revision control system, build system).
These systems can by provided by communities such as Github, Bitbucket or Fedora.

Providers can be categorized based on project origin as:

* upstream providers (original location of Go projects)
* distribution providers (location of downstreamed versions of Go projects)
* other provides (any kind of medium downstreaming upstream version of Go projects)

Each provider can consist of revision control systems. E.g. git, mercurial repository.
Or other systems such as packaging mechanism where each project is represented
as a distribution package.
Each such system can have mechanism to track history of project's evolution.
E.g. using commits, revisions or builds.

What a user actually uses at any given point of time is project snapshot (or its instance).
Each project snapshot corresponds to a commit in revision control system or build
in distribution builder system.

Thus, the ecosystem can be described as a hiearchy of resources starting from project snapshots.
Snapshots (e.g. commits or builds) of the same project are grouped into correponding system
such as repository (or package). Repositories and packages create project pools.
E.g. all projects in github.com, all projects in bitbucket.org, all Fedora 22 packages.
Based on the project origin, the final categorization (upstream providers, distribution providers)
closes the hiearchy.

## Project provider signature

To unambiguously determine project in a pool,
each one is assigned with a unique signature (fingerprint).

E.g. ``github.com/gofed/lib`` is described as:

```yaml
---
provider_type: upstream_repository
provider: github
username: gofed
project: lib
```

``gofed-lib`` package can correspond to:

```yaml
---
provider_type: distribution_package
product: fedora
version: 22
package: gofed-lib
```

## Project signature

To unambiguously determine project snapshots in entire ecosystem,
its location in revision control system or build system must be specified:

E.g. ``github.com/gofed/lib`` of ``b88165854fa7172ce0fdbdbe73234ce311f82465`` commit is described as:

```yaml
---
provider-type: upstream_repository
provider: github
username: gofed
project: lib
commit: b88165854fa7172ce0fdbdbe73234ce311f82465
```

``gofed-lib`` package of ``gofed-lib-0.0.10-3.fc22`` corresponds to:

```yaml
---
provider_type: distribution_package
product: fedora
version: 22
package: gofed-lib
build:
  name: gofed-lib-0.0.10-3.fc22
```

Additional refinement can be provided if needed. E.g. specifying distribution rpms:

```yaml
---
provider_type: distribution_package
product: fedora
version: 22
package: gofed-lib
build: 
  name: gofed-lib-0.0.10-3.fc22
  rpms:
    - name: gofed-lib-utils-0.0.10-3.fc22
    - name: gofed-lib-core-0.0.10-3.fc22
```

Or listing only subset of defined packages.

##TODO

* provide a list of all currently supported providers
* provide a list of possibly supported providers
* provide a string representation of signatures (an all its variants, e.g. "Fedora 22" = "f22" = "F22")
* use cases for signatures (e.g. check-deps, retrieval of source code tarball or rpm, scan of subset of ecosystem by partial signature specification)
