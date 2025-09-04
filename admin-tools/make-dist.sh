#!/bin/bash
PACKAGE=trepan3k_mathics3

# FIXME put some of the below in a common routine
function finish {
  if [[ -n "$trepan3k_mathics3_owd" ]] then
     cd $trepan3k_mathics3_owd
  fi
}

trepan3k_mathics3_owd=$(pwd)
cd $(dirname ${BASH_SOURCE[0]})
trap finish EXIT

cd ..
source $PACKAGE/version.py
echo $__version__

pyversion=3.13
if ! pyenv local $pyversion ; then
    exit $?
fi

rm -fr build
pip wheel --wheel-dir=dist .
python -m build --sdist
finish
