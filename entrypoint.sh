#!/bin/sh

pytest src/products/tests.py

if [ $? -eq 0 ]; then
    uvicorn src.main:app --reload --proxy-headers --host 0.0.0.0 --port 80
else
    echo "Tests failed, not starting the server."
    exit 1
fi