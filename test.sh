#!/bin/bash
set -ex
docker-compose pull
docker-compose up -d
python3 main.py
