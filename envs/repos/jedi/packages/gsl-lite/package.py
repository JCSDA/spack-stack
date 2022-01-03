# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class GslLite(CMakePackage):
    """gsl-lite – A single-file header-only version of ISO C++ Guidelines Support Library (GSL) for C++98, C++11, and later"""
    homepage = "https://github.com/gsl-lite/gsl-lite"
    git = "https://github.com/gsl-lite/gsl-lite.git"
    url = "https://github.com/gsl-lite/gsl-lite/archive/0.37.0.zip"

    version('0.40.0', commit='d6c8af99a1d95b3db36f26b4f22dc3bad89952de')
    version('0.39.0', commit='d0903fa87ff579c30f608bc363582e6563570342')
    version('0.38.1', commit='e1c381746c2625a76227255f999ae9f14a062208')
    version('0.37.0', commit='4b796627ad0fa42640f5fdb96f23c4a0d9ee084f')
    version('0.34.0', commit='93607223a48621dae3cedd6b3335431b38067fae')


