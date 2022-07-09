#!/bin/bash
set -e

poetry install
poetry run python src/test.py