### Location of Go projects

1. List of imported paths
2. ip -> provider (upstream repository, distribution package, distribution collection, ...)
3. provider -> project signature

Each projects imports a set of Go packages.
Imported packages/paths can be decomposed into prefix classes.
Each prefix class is provided by exactly one source code unit, e.g. project, set of distribution rpms (subset of build).
Each source code unit can by uniquely determined. Each source code unit corresponds to repository + commit 

ProjectSnapshot
-ProjectDistributionSnapshot(distribution provider [+ build/rpm] -> project location + build date + maintainer + known issues + statistics + ... )
--ProjectFedoraDistributionSnapshot
--ProjectRHELDistributionSnapshot
--ProjectCentOSDistributionSnapshot
-ProjectRepositorySnapshot(repository provider [+ commit] -> project location + commit author + commit date + known issues + statistics + ...)
--ProjectGithubRepositorySnapshot
--ProjectBitbucketRepositorySnapshot
--ProjectGooglecodeRepositorySnapshot
-ProjectDistributionCollectionSnapshot or extension of ProjectDistributionSnapshot?
-Project???Snapshot

Does ProjectSnapshot comparison make sense?
Each snapshot kind (Repository, Distribution, ...) have different content in general.
Assuming each snapshot must contain origin repository commit, only commit comparison can be carried.
If the commit is not present (e.g. project is not managed by any revision system), the comparison fails.
What are the common data then?
- commit (commit of the project or commit packaged/captured in distribution/other storage medium)
- provider signature (repository, distribution, collection, ...)
- other numbers (trend, healthiness, ...)

One prefix can be spread across two or more rpms (e.g. influxdb). In general by a set of devel subpackages of a given package.

### Providers

Unique location of source code provider. E.g.

* upstream repository (github.com, bitbucket.org),
* distribution builder (Fedora:f24:PKGNAME)

### ProjectSnapshots

UpstreamRepositoryResourceUnitInfo
- GithubRepositoryResource
- BitbucketRepsitoryResource
DistributionPackageResource
- FedoraResource (e.g. Fedora:f24:etcd:etcd-2.2.2-1.fc24:etcd-devel-2.2.2-1.fc24.noarch.rpm)
- RHELResource
- CentOSResource

UpstreamRepositoryProvider (github, bitbucket) -> UpstreamRepository (username, project) -> ProjectSignature (commit)
DistributionPackageProvider (Fedora:f24) -> DistributionPackage (package) -> ProjectSignature(build)

Provider -> ProjectPool -> ProjectSignature. Signature consists of provider and resource

"There is only one true provider and it is upstream."

Unique location of source code unit inside a provider. E.g.

* upstream repository (provider + commit)
* distribution builder (provider + build)

Use cases:

* determine location of rpms (e.g. for url builder to generate rpm download url or for resource providers)
