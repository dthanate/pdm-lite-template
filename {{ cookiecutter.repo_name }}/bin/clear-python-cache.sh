#!/bin/bash
DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd $DIR/..
find . -type d -name '__pycache__' | xargs -r rm -r
find . -type d -name '.ipynb_checkpoints' | xargs -r rm -r
find . -type d -name '.virtual_documents' | xargs -r rm -r
find . -type d -name '.mypy_cache' | xargs -r rm -r
find . -type d -name '.pytest_cache' | xargs -r rm -r
find . -type d -name '.hypothesis' | xargs -r rm -r
