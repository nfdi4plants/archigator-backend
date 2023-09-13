#!/bin/bash

set -e

echo "starting archigator..."

echo "starting uvicorn"
uvicorn --workers 10 --host 0.0.0.0 --port 8000 main:app
