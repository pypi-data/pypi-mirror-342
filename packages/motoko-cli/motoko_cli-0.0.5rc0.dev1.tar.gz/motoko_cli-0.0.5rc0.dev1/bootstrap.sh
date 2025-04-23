#!/bin/bash

if [ "$CI" != "" ]; then
  git config --global --add safe.directory /app
  git config --global --add safe.directory /github/workspace
fi

version_file="src/motoko_cli/__about__.py"
tmp_version_file="src/motoko_cli/__about__-tmp.py"
base_version="0.0.1rc0.dev0"

if [ "$CI" != "" ]; then
  git_hash=$(git rev-parse --short HEAD)
  latest_tag=$(git describe --tags --abbrev=0)
  new_version=$(python -c "print('$latest_tag'.split('.dev')[0] + '.dev' + str(int('$latest_tag'.split('.dev')[1])+1))")
  echo "New version will be $new_version"
  python -c "open('$tmp_version_file', 'w', encoding='utf-8').write(open('$version_file', 'r', encoding='utf-8').read().replace('$base_version', '$new_version')); import shutil; shutil.move('$tmp_version_file', '$version_file')"
fi

rm -rf ./dist
hatch build

pip install .
pytest ./tests --junitxml=python-report.xml
