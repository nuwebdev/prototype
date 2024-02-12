venv:
	conda env update -f environment.yml --prune

run:
	flask --app flaskr/__init__.py run --debug

