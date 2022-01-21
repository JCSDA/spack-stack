# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class AppleClang(Package):
    """Meta package to 'install' the native Apple clang compiler in spack."""

    homepage = "https://opensource.apple.com/projects/llvm-clang"
    url = "https://notavalidurl.com/notavalidfile.tar.gz"

    maintainers = ['climbfuji']

    version('13.0.0')

    def install(self, spec, prefix):
        raise InstallError("apple-clang is a meta package that cannot be installed")
