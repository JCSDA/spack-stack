# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: Apache-2.0

import os
import sys

from spack import *

class JediEnv(BundlePackage):
    """Development environment for JEDI"""

    # DH* TODO UPDATE
    homepage = "https://github.com/JCSDA/jedi-stack"
    git      = "https://github.com/JCSDA/jedi-stack.git"

    maintainers = ['climbfuji']

    version('main', branch='main')

    depends_on('jedi-fv3-bundle-env', type='run')
    depends_on('jedi-um-bundle-env',  type='run')
    depends_on('jedi-ufs-bundle-env', type='run')
    depends_on('jedi-tools-env',      type='run')
