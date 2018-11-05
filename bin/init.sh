#!/usr/bin/env bash

set -e

if [ -z $1 ] ; then
	echo "Usage: $0 <absolute path to your Google App Engine SDK>"
	exit 1
fi

echo "==== Initializing environment ===="

echo "... Installing pip dependencies ..."

rm -rf venv libs
virtualenv venv
source venv/bin/activate
venv/bin/pip2 install -r requirements.txt -t libs/
venv/bin/pip2 install -r dev_requirements.txt

echo "... Adding paths to venv ..."

current_path=$(pwd)
venv_lib_path=${current_path}"/venv/lib/python2.7/site-packages/lib.pth"
echo ${current_path}"/libs/" >> ${venv_lib_path}
echo $1 >> ${venv_lib_path}
echo $1"/lib/" >> ${venv_lib_path}
echo $1"/lib/yaml/lib" >> ${venv_lib_path}
