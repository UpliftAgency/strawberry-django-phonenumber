#!/usr/bin/env bash
# Run with --check for CI (no file modifications). Default: format/fix locally.
set -euo pipefail

CHECK=false
if [[ "${1:-}" == "--check" ]]; then
  CHECK=true
fi

TARGETS=(strawberry_django_phonenumber tests test_app)

if $CHECK; then
  poetry run autoflake --check --recursive \
    --remove-all-unused-imports --remove-duplicate-keys --remove-unused-variables \
    "${TARGETS[@]}"
  poetry run black --check .
  poetry run isort --check-only "${TARGETS[@]}"
  poetry run flake8 "${TARGETS[@]}"
  poetry run ssort --check "${TARGETS[@]}"
  poetry run bandit -r strawberry_django_phonenumber/ test_app/
  poetry run pip-audit
else
  poetry run autoflake --in-place --recursive \
    --remove-all-unused-imports --remove-duplicate-keys --remove-unused-variables \
    "${TARGETS[@]}"
  poetry run flake8 "${TARGETS[@]}"
  poetry run bandit -r strawberry_django_phonenumber/ test_app/
  poetry run ssort "${TARGETS[@]}"
  poetry run isort "${TARGETS[@]}"
  poetry run black .
fi
