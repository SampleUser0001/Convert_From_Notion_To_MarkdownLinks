#!/bin/bash

source common.sh

pushd src > /dev/null
for d in `find . -type d ` ; do
    echo ${d}
    python -m unittest discover -v ${d}
done 

popd

