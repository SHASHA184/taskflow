#!/bin/bash

# Load test data into the database
docker compose exec app python app/load_test_data.py