#!/usr/bin/env bash
set -euo pipefail

export POETRY_KEYRING_ENABLED=false

poetry install -E psycopg
