#!/bin/bash
# build.sh
set -e

if [ ! -d "env" ]; then
    echo "No virtual environment found! Run setup_env.sh first."
    exit 1
fi

if [ ! -f "env/bin/pyinstaller" ]; then
    ./env/bin/pip install pyinstaller
fi

./env/bin/pyinstaller build.spec
