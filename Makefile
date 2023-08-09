## Check code quality
chk: check
lint: check
check: flake black_check isort_check

cov: coverage

fmt: format
format: isort black

tst_m: test_m
tst_f: test_f
tst_a: test_a

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

test_m:
	cd superlists && python manage.py test lists accounts && cd ..

test_f:
	cd superlists && python manage.py test functional_tests && cd ..

test_a:
	cd superlists && python manage.py test && cd ..
