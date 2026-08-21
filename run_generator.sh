#!/bin/bash
PROJECT_DIR="/home/ravi/Desktop/Study Material/Projects/Personal/twitter-automation"
cd "$PROJECT_DIR" || exit 1
exec "$PROJECT_DIR/venv/bin/python" generate_post.py
