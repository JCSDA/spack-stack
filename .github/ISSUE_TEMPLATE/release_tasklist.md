---
name: Release task list
about: Create a task list for a spack-stack release
title: '[RELEASE] release-x.y.z tasks'
labels: ''
assignees:
# EPIC
- natalie-perlin
- ratkovasic-noaa
- rickgrubin-noaa
# JCSDA
- ashley314
- eap
# NASA
- mathomp4
# NOAA
- alexanderrichert-noaa
- hanglei-noaa
# NRL
- climbfuji

---

## Release task list

Project board: _insert link here_

- [ ] Create release branches `release/x.y` for spack, spack-packages, and spack-stack (update `.gitmodules` in spack-stack accordingly)
- [ ] Clear project board (no open pull requests other than for specific site configs or documentation)
- [ ] Prepare Wiki page for release (https://github.com/jcsda/spack-stack/wiki)
- [ ] Roll out release x.y.z from release branch `release/x.y` and update documentation (readthedocs), site config, and wiki page each time
    - [ ] Acorn (NOAA-EMC)
    - [ ] Atlantis (NRL)
    - [ ] Blueback (NRL)
    - [ ] Derecho (EPIC)
    - [ ] Discover (JCSDA)
    - [ ] Gaea (EPIC)
    - [ ] Hercules (EPIC)
    - [ ] Narwhal (NRL)
    - [ ] NAS (NASA)
    - [ ] Nautilus (NRL)
    - [ ] Orion (EPIC)
    - [ ] S4 (???)
    - [ ] Ursa (EPIC)
    - [ ] JCSDA AWS Parallelcluster (JCSDA)
    - [ ] JCSDA AWS AMI (JCSDA)
    - [ ] JCSDA CI containers (JCSDA)
    - [ ] NAVY PW AWS (NRL)
    - [ ] NOAA PW AWS (EPIC)
    - [ ] NOAA PW Azure (EPIC)
    - [ ] NOAA PW Gcloud (EPIC)
- [ ] Tag repositories spack, spack-packages, and spack-stack ((update `.gitmodules` in spack-stack accordingly)
- [ ] Finalize Wiki page for release (https://github.com/jcsda/spack-stack/wiki)
- [ ] Prepare and publish release notes: https://github.com/JCSDA/spack-stack/releases
- [ ] As needed, merge pull requests into release branches back into `develop` / `spack-stack-dev`
- [ ] Close GitHub project
