## Overview

To avoid hardcoding specs in the generic container recipes, we keep the specs list empty (`specs: []`) and manually add the specs for the particular spack-stack release and application as listed below, *after* running `spack stack create ctr`.

### spack-stack-1.1.0 / skylab-2.0.0 containers
```
  specs: [base-env@1.0.0, jedi-base-env@1.0.0 ~fftw, jedi-ewok-env@1.0.0, jedi-fv3-env@1.0.0,
    jedi-mpas-env@1.0.0, jedi-ufs-env@1.0.0, bacio@2.4.1,
    bison@3.8.2, bufr@11.7.0, ecbuild@3.6.5, eccodes@2.25.0, ecflow@5,
    eckit@1.19.0, ecmwf-atlas@0.29.0 +trans ~fftw, ectrans@1.0.0 ~fftw, eigen@3.4.0,
    fckit@0.9.5, flex@2.6.4, fms@release-jcsda, g2@3.4.5, g2tmpl@1.10.0, gftl-shared@1.5.0,
    gsibec@1.0.5, hdf5@1.12.1, hdf@4.2.15, ip@3.3.3, jasper@2.0.32, jedi-cmake@1.3.0,
    libpng@1.6.37, nccmp@1.9.0.1, netcdf-c@4.8.1, netcdf-cxx4@4.3.1,
    netcdf-fortran@4.5.4, nlohmann-json-schema-validator@2.1.0, nlohmann-json@3.10.5,
    parallel-netcdf@1.12.2, parallelio@2.5.4, py-f90nml@1.4.2, py-numpy@1.22.3,
    py-pandas@1.4.0, py-pyyaml@6.0, py-scipy@1.8.0, py-shapely@1.8.0, py-xarray@2022.3.0,
    sp@2.3.3, udunits@2.2.28, w3nco@2.4.1, nco@5.0.6,
    yafyaml@0.5.1, zlib@1.2.12, odc@1.4.5, crtm@v2.3-jedi.4]
    # Don't build ESMF and MAPL for now:
    # https://github.com/JCSDA-internal/MPAS-Model/issues/38
    # https://github.com/NOAA-EMC/spack-stack/issues/326
    # esmf@8.3.0b09, mapl@2.12.3
```