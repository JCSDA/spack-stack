# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: Apache-2.0

import os
from spack import *

class JediCmake(CMakePackage):
    """CMake/ecbuild toolchains to facilitate portability on different systems."""

    homepage = "https://github.com/JCSDA-internal/jedi-cmake"
    git = "https://github.com/JCSDA-internal/jedi-cmake.git"
    url = "https://github.com/JCSDA-internal/jedi-cmake/archive/1.0.0.zip"

    maintainers = ['rhoneyager']

    version('master', branch='master', no_cache=True)
    version('develop', branch='develop', no_cache=True)
    version('1.2.0', url="https://github.com/JCSDA/jedi-cmake/archive/refs/tags/1.2.0.tar.gz", sha256='eb9f1c403d1b43a90a5e774097382b183d56d5b40a1204b51af2da8db1559b21', preferred=True)
    version('1.1.0', url="https://github.com/JCSDA/jedi-cmake/archive/refs/tags/1.1.0.tar.gz", sha256='f1fe41eb5edd343bdf57eb76bea6d1b9f015878f0a9d0eb1e9dba18b903d3b35')
    version('1.0.0', url="https://github.com/JCSDA/jedi-cmake/archive/refs/tags/1.0.0.tar.gz", sha256='d773a800350e69372355b45e89160b593818cd438a86925b8a689c47996a0b9a')

    depends_on('cmake @3.10:', type=('build'))

