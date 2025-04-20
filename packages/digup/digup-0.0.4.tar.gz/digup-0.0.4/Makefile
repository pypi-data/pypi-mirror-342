format:
	ruff check --fix
	black .

test:
	mypy .
	pytest

coverage:
	coverage run -m pytest && coverage html && open htmlcov/index.html

check: format test

clean:
	rm -f .coverage
	rm -rf .pytest_cache
	rm -rf .ruff_cache
	rm -rf htmlcov
	rm -f dist/*

release: clean
	python -m build
	python -m twine upload dist/*