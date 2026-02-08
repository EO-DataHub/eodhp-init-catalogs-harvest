## eodhp-init-catalogs-harvest
### Repository to trigger harvesting of top-level STAC Catalogs into Resource Catalog

This repository contains code to trigger harvesting of the top-level STAC Catalogs for loading into the Resource Catalogue. Currently this includes the `user-datasets` and `supported-datasets` top-level catalogs. Triggers are sent via Pulsar. This harvest is required before user-datasets can be ingested from workflow executions.

## Installation

### Prerequisites

- [uv](https://docs.astral.sh/uv/)

### Install via makefile

```commandline
make setup
```

This will install dependencies via `uv sync` and set up `pre-commit` hooks.

It's safe and fast to run `make setup` repeatedly as it will only update these things if
they have changed.

After `make setup` you can run `make pre-commit` to run pre-commit checks on staged changes and
`make pre-commit-all` to run them on all files.

### Running the service

Set up environment variables:

```commandline
export PULSAR_URL=<pulsar_url>
```

Run the service:

```commandline
uv run python -m init_catalogs
```

## Building and testing

This component uses `pytest` tests and the `ruff` linter/formatter.

A number of `make` targets are defined:

- `make test`: run tests continuously (watch mode)
- `make testonce`: run tests once
- `make format`: format and auto-fix lint issues
- `make check`: run all linting and type checks
- `make dockerbuild`: build a `latest` Docker image (use `make dockerbuild VERSION=1.2.3` for a release image)
- `make dockerpush`: push a `latest` Docker image (again, you can add `VERSION=1.2.3`) - normally this should be done
  only via the build system and its GitHub actions.

## Notes
This repo also includes workflows to build and push a docker image to a remote repository upon merge and release.
