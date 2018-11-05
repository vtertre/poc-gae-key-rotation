#!/usr/bin/env bash

set -e

if [ -z $1 ] || [ -z $2 ] ; then
	echo "Usage: $0 <version> <gcloud account>"
	exit 1
fi

echo "==== Configuring dependencies for production ===="

rm -rf venv libs
virtualenv venv
source venv/bin/activate
venv/bin/pip2 install -r requirements.txt -t libs/

echo "==== Deploying app to App Engine ===="

gcloud app deploy \
    api.yaml \
    --account=$2 \
    --project=TODO \
    --version=$1 \
    --no-promote \
    --quiet
