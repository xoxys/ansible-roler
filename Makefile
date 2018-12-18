PYTHON_LINT=flake8 flake8-colors pep8-naming
PYTHON_TEST=pytest pytest-cov pytest-mock

prepare:
	apk add --no-cache openssl-dev libffi-dev build-base
	pip install --upgrade pip setuptools wheel virtualenv -q

test:
	virtualenv /env-test
	env /env-test/bin/pip install ${PYTHON_TEST} -q
	env /env-test/bin/pip install -e -q .
	env /env-test/bin/pytest --cov=ansibleroler tests/ -v

lint:
	virtualenv /env-lint
	env /env-lint/bin/pip install ${PYTHON_LINT} -q
	env /env-lint/bin/flake8 ansibleroler
