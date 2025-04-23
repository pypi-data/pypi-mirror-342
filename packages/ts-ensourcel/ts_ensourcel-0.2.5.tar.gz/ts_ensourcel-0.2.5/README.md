# {{ NAME }} - The default project.

[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-green.svg?style=flat-square)](https://conventionalcommits.org)
[![PyPI](https://img.shields.io/pypi/v/{{ NAME }}?style=flat-square)](https://pypi.org/project/{{ NAME }}/)
![Maintenance](https://img.shields.io/maintenance/yes/2025?style=flat-square)

Default to using justfile as local script holder
Testing out using uv
Using poetry for management, etc.

# Getting started

1. The placeholder names used throughout are not all consistent at all.
Sorry.
Iteratively bug slaying should get you there.

2. Get a dev shell to play around.
Probably allowing direnv will be the easiest startup.
Remember that it won't work until you fix all the placeholder names and make an initial commit.
So

3. Do that.

## dev

Build with `just`, preferred over `do.sh` I think.

## CLI

Details of how to use this cli in this project

## Build

Builds on both nix and via uv tools, tests run both ways as well.
No need to use nix to build the pypi upload versions.

## CI

Attempts to use a cache on gitea actions.
