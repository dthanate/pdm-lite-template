#!/usr/bin/env bash
mv .env_ .env
mv .envrc_ .envrc
mv .gitignore_ .gitignore
pdm venv --python {{ cookiecutter.python_executable }} create
mkdir -p .venv/etc/ptpython
mv ptpython_config.py_ .venv/etc/ptpython/config.py
pdm install -G all
git init
git add .
git commit -m "initial commit"
exit 0
