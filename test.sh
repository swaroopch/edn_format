#!/usr/bin/env bash

ENVNAME=$(basename `pwd`)
conda env remove -yq -n $ENVNAME &> /dev/null
conda create -yq -n $ENVNAME python pip #1> /dev/null
source activate $ENVNAME
pip install -e .
py.test -f
