## eodhp-init-catalogs-harvest
### Repository to trigger harvesting of top-level STAC Catalogs into Resource Catalog

This repository contains code to trigger harvesting of the top-level STAC Catalogs for loading into the Resource Catalogue. Currently this includes the `user-datasets` and `supported-datasets` top-level catalogs. Triggers are sent via Pulsar. This harvest is required before user-datasets can be ingested from workflow executions.

## Installation

### Install via makefile

```commandline
make setup
```

This will create a virtual environment called `venv`, build `requirements.txt` and
`requirements-dev.txt` from `pyproject.toml` if they're out of date, install the Python
and Node dependencies and install `pre-commit`.

It's safe and fast to run `make setup` repeatedly as it will only update these things if
they have changed.

After `make setup` you can run `pre-commit` to run pre-commit checks on staged changes and
`pre-commit run --all-files` to run them on all files. This replicates the linter checks that
run from GitHub actions.


### Alternative installation

1. Follow the instructions [here](https://github.com/UKEODHP/template-python/blob/main/README.md) for installing a
   Python 3.11 environment.
2. Install dependencies:

```commandline
pip3 install -r requirements.txt
```

3. Set up environment variables

```commandline
export PULSAR_URL=<pulsar_url>
```

4. Run the service

```commandline
python -m init_catalogs
```

## Building and testing

This component uses `pytest` tests and the `ruff` and `black` linters. `black` will reformat your code in an
opinionated way.

A number of `make` targets are defined:

- `make test`: run tests continuously
- `make testonce`: run tests once
- `make lint`: lint and reformat
- `make dockerbuild`: build a `latest` Docker image (use `make dockerbuild `VERSION=1.2.3` for a release image)
- `make dockerpush`: push a `latest` Docker image (again, you can add `VERSION=1.2.3`) - normally this should be done
  only via the build system and its GitHub actions.


## Notes
This repo also includes workflows to build and push a docker image to a remote repository upon merge and release.
