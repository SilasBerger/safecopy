#!/bin/bash

files=(handler.py logging.py README.md LICENSE LICENSE_IMAGEMAGICK scan-extensions.py venv/)
repo_name="safecopy"

command="tar czf ${repo_name}.tar.gz"
for f in ${files[*]}; do
  command="${command} ../$repo_name/$f"
  echo "$command"
done

 $command
