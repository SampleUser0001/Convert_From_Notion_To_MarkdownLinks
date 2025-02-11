#!/bin/bash

source common.sh

pushd src > /dev/null
if [ $# -eq 0 ]; then
    for d in `find . -type d ` ; do
        echo ${d}
        python -m unittest discover -v ${d}
    done 
else
    python -m unittest $1
fi
popd

