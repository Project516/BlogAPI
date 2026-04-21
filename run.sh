#!/bin/sh

uv format
uv audit
uv run main.py --reload