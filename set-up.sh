#!/usr/bin/env bash

docker-compose -f docker-compose.yml up -d --build

conda create --name meli-challenge python=3.8 pip psycopg2
conda activate meli-challenge

pip install -r requirements.txt