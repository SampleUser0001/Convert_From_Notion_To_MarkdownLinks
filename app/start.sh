#!/bin/bash

source common.sh

pushd src > /dev/null
python app.py
# 起動引数を渡したい場合は下記。
# python app.py $1 $2 ...

popd > /dev/null