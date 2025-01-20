#!/bin/bash
PACKAGE=Mathics3-trepan

# FIXME put some of the below in a common routine
function finish {
  if [[ -n "$trepan3k_mathics3_owd" ]] then
     cd $trepan3k_mathics3_owd
  fi
}

cd $(dirname ${BASH_SOURCE[0]})
trepan3k_mathics3_owd=$(pwd)
trap finish EXIT

if ! source ./pyenv-versions ; then
    exit $?
fi


cd ..
source pymathics/natlang/version.py
echo $__version__

pyversion=3.12
if ! pyenv local $pyversion ; then
    exit $?
fi

python setup.py bdist_wheel --universal
mv -v dist/${PACKAGE}-${__version__}-{py2.,}py3-none-any.whl
python ./setup.py sdist
finish
