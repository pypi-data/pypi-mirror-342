# hello-world - The default project (change me).

[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-green.svg?style=flat-square)](https://conventionalcommits.org)
[![PyPI](https://img.shields.io/pypi/v/{{ NAME }}?style=flat-square)](https://pypi.org/project/{{ NAME }}/)
![Maintenance](https://img.shields.io/maintenance/yes/2025?style=flat-square)

Default to using justfile as local script holder
Testing out using uv
Using poetry for management, etc.
In nix, nix fmt does formatting for everything.

# Getting started

1. You may need to initialise a git repository.
 * `git init`, `git add .`, `git commit -m "initial commit"`

2. Double check if you need to update nixpkgs, update python version etc.
 * in nix, some version of `nix flake update`, changing python version in flake.nix etc.

3. The placeholder names used throughout are not all consistent at all.
Sorry.
Iteratively bug slaying should get you there.

4. Get a dev shell to play around.
Probably allowing direnv will be the easiest startup.
Remember that it won't work until you fix all the placeholder names and make an initial commit.
So

5. Do that.

## dev

Build with `just`, preferred over `do.sh` I think.

## CLI

Details of how to use this cli in this project
