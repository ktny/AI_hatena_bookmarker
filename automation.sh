#!/bin/bash
set -euxo pipefail

sudo docker compose run --rm app python hotentry.py
sudo docker compose run --rm app python newentry.py
