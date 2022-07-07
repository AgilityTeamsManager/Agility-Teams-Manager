#!/usr/bin/sh
#TODO: GitHub Action
poetry lock --no-update -q --no-ansi -n
poetry export -f requirements.txt -o requirements.txt --without-hashes -q --no-ansi -n