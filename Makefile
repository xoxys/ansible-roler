PYTHON_LINT=flake8 flake8-colors pep8-naming
PYTHON_TEST=pytest pytest-cov pytest-mock

prepare:
	apk add --no-cache openssl-dev libffi-dev build-base
	pip install --upgrade pip setuptools wheel virtualenv -q

test:
	virtualenv /env-test
	. /env-test/bin/activate
	pip install ${PYTHON_TEST} -q
	pip install . -q
	pytest --cov=ansibleroler tests/ -v
	deactivate

lint:
	virtualenv /env-lint
	. /env-lint/bin/activate
	pip install ${PYTHON_LINT} -q
	flake8 ansibleroler
	deactivate
