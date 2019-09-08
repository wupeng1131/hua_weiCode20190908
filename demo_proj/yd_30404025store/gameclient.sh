#!/bin/bash
cd "$(dirname "$0")"
cd client
#pip install numpy -i https://pypi.tuna.tsinghua.edu.cn/simple
#pip install Cython --install-option="--no-cython-compile" -i https://pypi.tuna.tsinghua.edu.cn/simple
sh start.sh $1 $2 $3
