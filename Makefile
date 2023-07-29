## Check code quality
chk: check
lint: check
check: flake black_check isort_check

cov: coverage

fmt: format
format: isort black

isort:
	isort superlists

isort_check:
	isort --check-only superlists


black:
	black --config pyproject.toml superlists

black_check:
	black --config pyproject.toml --diff --check superlists


flake:
	flake8 --config .flake8 superlists


coverage:
	cd superlists && coverage run manage.py test lists && coverage report -m && cd ..
