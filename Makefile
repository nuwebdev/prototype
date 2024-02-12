venv:
	conda create flaskr
	conda activate flaskr

run:
	flask --app flaskr/__init__.py run --debug

