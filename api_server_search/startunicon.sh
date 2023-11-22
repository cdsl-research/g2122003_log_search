#!/bin/bash
set -eux

. .venv/bin/activate
pip install -r requirements.txt
uvicorn search_index_ver8:app --reload --host=0.0.0.0
