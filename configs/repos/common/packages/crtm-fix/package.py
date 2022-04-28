# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class CrtmFix(Package):
    """CRTM coeffecient files"""

    homepage = "https://github.com/NOAA-EMC/crtm"
    url      = "ftp://ftp.ucar.edu/pub/cpaess/bjohns/fix_REL-2.3.0_emc.tgz"

    maintainers = ['kgerheiser']

    version('2.4.0_emc', sha256='60e41f97e4b46bb84f252c9fc2e88cf765835aa94f9caa8e1d4dc3f57e3fbdf2')
    version('2.3.0_emc', sha256='fde73bb41c3c00666ab0eb8c40895e02d36fa8d7b0896c276375214a1ddaab8f')

    variant('big_endian', default=True, description='Install big_endian fix files')
    variant('little_endian', default=False, description='Install little endian fix files')
    variant('netcdf', default=True, description='Install netcdf fix files')

    conflicts('+big_endian', when='+little_endian', msg='big_endian and little_endian conflict')

    def url_for_version(self, version):
        url = 'ftp://ftp.ucar.edu/pub/cpaess/bjohns/fix_REL-{}.tgz'
        return url.format(version)

    def install(self, spec, prefix):
        spec = self.spec
        
        endian_dirs = []
        if '+big_endian' in spec:
            endian_dirs.append('Big_Endian')
        elif '+little_endian' in spec:
            endian_dirs.append('Little_Endian')

        if '+netcdf' in spec:
            endian_dirs.extend(['netcdf', 'netCDF'])

        fix_files = []
        for d in endian_dirs:
            fix_files = fix_files + find('.', '*/{}/*'.format(d))

        mkdir(self.prefix.fix)
        cwd = pwd()

        # Big_Endian amsua_metop-c.SpcCoeff.bin is incorrect
        # Little_Endian amsua_metop-c_v2.SpcCoeff.bin is what it's supposed to be
        # Remove the incorrect file, and install it as noACC, and install the correct file
        if '+big_endian' in spec and spec.version == Version('2.4.0_emc'):
            fix_files.remove(join_path(cwd, 'SpcCoeff','Big_Endian', 'amsua_metop-c.SpcCoeff.bin'))

            install(join_path('SpcCoeff', 'Big_Endian', 'amsua_metop-c.SpcCoeff.bin'),
                join_path(self.prefix.fix, 'amsua_metop-c.SpcCoeff.noACC.bin'))

            install(join_path('SpcCoeff', 'Little_Endian', 'amsua_metop-c_v2.SpcCoeff.bin'), 
                join_path(self.prefix.fix, 'amsua_metop-c.SpcCoeff.bin'))

        for f in fix_files:
            install(f, self.prefix.fix)

    def setup_run_environment(self, env):
        env.set('CRTM_FIX', self.prefix.fix)
