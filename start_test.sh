#!/bin/bash

source venv/bin/activate

pushd app > /dev/null

ln -s $(pwd)/src/$1.env $(pwd)/src/.env

# 引数の数に応じて変更する
# bash start.sh $1 $2 ...
bash unittest.sh

unlink $(pwd)/src/.env

popd > /dev/null

deactivate