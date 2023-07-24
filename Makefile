## Check code quality
chk: check
lint: check
check: flake black_check isort_check


fmt: format
format: isort black

isort:
	isort tests

isort_check:
	isort --check-only tests


black:
	black --config pyproject.toml tests

black_check:
	black --config pyproject.toml --diff --check tests


flake:
	flake8 --config .flake8 tests
