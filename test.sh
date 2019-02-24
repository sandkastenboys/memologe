#!/bin/bash
set -ex
docker-compose pull
docker-compose up -d
sleep 10
python3 main.py
