from lib.utils import runCommand
import os

class ExtractionException(Exception):
    pass

class ApiExtractor(object):

    def __init__(self, gopath, generated, package_path, hexsha, depsfile, cgodir = ""):
        # GOPATH/src directory containing all required dependencies
        self._gopath = gopath
        # Go stlib and preloaded artefacts
        self._generated = generated
        # CGO symbol table
        self._cgo = cgodir
        # Project entry point
        self._package_path = package_path
        self._hexsha = hexsha
        # Dependency snapshot
        self._depsfile = depsfile

        self._so = ""


    # Just call the go binary with valid input
    def extract(self):
        options = [
            "--package-path {}".format(self._package_path),
            "--package-prefix {}:{}".format(self._package_path, self._hexsha),
            "--symbol-table-dir {}".format(self._generated),
            "--library",
        ]

        if self._cgo != "":
            options.append("--cgo-symbols-path {}".format(self._cgo))

        if self._depsfile.endswith("glide.lock"):
            options.append("--glidefile {}".format(self._depsfile))
        elif self._depsfile.endswith("Godeps.json"):
            options.append("--godepsfile {}".format(self._depsfile))
        else:
            raise ValueError("Dependency file {} not recognized".format(self._depsfile))

        self._so, se, rc = runCommand("GOPATH={} goextract {}".format(self._gopath, " ".join(options)))
        if rc != 0:
            raise ExtractionException("goextract({}): {}".format(rc, se))

        return self

    def stdout(self):
        return self._so
