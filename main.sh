#!/bin/bash
export PYTHONPATH=.
python3 src/main.py

# Serve the public directory
cd public && python3 -m http.server 8888
