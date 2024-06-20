.PHONY: dockerbuild dockerpush test testonce ruff pylint black lint
VERSION ?= latest
IMAGENAME = eodhp-init-catalog-ingest
DOCKERREPO ?= 312280911266.dkr.ecr.eu-west-2.amazonaws.com

dockerbuild:
	DOCKER_BUILDKIT=1 docker build -t ${IMAGENAME}:${VERSION} .

dockerpush: dockerbuild testdocker
	docker tag ${IMAGENAME}:${VERSION} ${}DOCKERREPO}/${IMAGENAME}:${VERSION}
	docker push ${DOCKERREPO}/${IMAGENAME}:${VERSION}

test:
	./venv/bin/ptw init-catalogs

testonce:
	./venv/bin/pytest tests

pylint:
	./venv/bin/pylint init-catalogs

ruff:
	./venv/bin/ruff .

black:
	./venv/bin/black .

lint: ruff black