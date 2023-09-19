#!/bin/bash
poetry run autoflake --in-place --recursive --remove-all-unused-imports --remove-duplicate-keys --remove-unused-variables strawberry_django_phonenumber tests test_app
poetry run flake8 strawberry_django_phonenumber tests test_app
poetry run bandit -r strawberry_django_phonenumber/
poetry run ssort strawberry_django_phonenumber tests test_app
poetry run isort strawberry_django_phonenumber tests test_app
poetry run black .
