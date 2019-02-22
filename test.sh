#!/bin/bash
set -x
docker-compose pull
docker-compose up -d
python3 main.py
