#!/bin/bash
set -euxo pipefail

docker compose run --rm app python hotentry.py
docker compose run --rm app python newentry.py
