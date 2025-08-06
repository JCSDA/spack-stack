## Description

_Note. The title and description will be used as commit log title and message for squash merges._

### Dependencies

_If there are PRs that need to be merged before or along with this one, please add "- [ ] waiting on LINK_TO_PR" for each of them._

### Issues addressed

_Add any issues here that this PR closes or is related to. Use "Resolves" or "Closes" to automatically close issues when the PR is merged. Using "Working towards" or "Related to" for other cases._

### Applications affected

List all known applications (UFS WM, JEDI, SRW, etc.) intentionally or unintentionally affected by this PR.

### Systems affected

List all systems intentionally or unintentionally affected by this PR.

## Testing

- CI: _Note whether the automatic tests (GitHub actions tests that run automatically for every commit) pass or not_
    - [ ] GitHub actions CI tests pass
    - [ ] GitHub actions CI tests do not pass (_provide explanation_)
    - [ ] GitHub actions CI tests skipped (_provide explanation if necessary_)
- New tests added: _List and describe any new tests added to GitHub actions_
    - [ ] ...
- Additional testing: _Add information on any additional tests conducted_
    - [ ] ...

## Checklist

- [ ] This PR addresses one issue/problem/enhancement or has a very good reason for not doing so.
- [ ] These changes have been tested on the affected systems and applications.
- [ ] All dependency PRs/issues have been resolved and this PR can be merged.
- [ ] All necessary updates to the documentation on readthedocs are included in this PR
    - For site config updates, check in particular `doc/source/PreConfiguredSites.rst` and `doc/source/MaintainersSection.rst`
- [ ] All necessary updates to the spack-stack wiki will be made when this PR is merged
