#!/usr/bin/env bash

set -e

if [ -z $1 ] || [ -z $2 ] ; then
	echo "Usage: $0 <version> <gcloud account>"
	exit 1
fi

echo "==== Configuring dependencies for production ===="

if [ ! -d "venv" ]; then
    virtualenv venv
    source venv/bin/activate
fi

rm -rf libs
venv/bin/pip2 install -r requirements.txt -t libs/

echo "==== Configuring app for production ===="

perl -pi -e "s/'dev'/'staging'/g" api.yaml

echo "==== Deploying app to App Engine ===="

gcloud app deploy \
    api.yaml \
    --account=$2 \
    --project=sandbox-vincent \
    --version=$1 \
    --quiet

perl -pi -e "s/'staging'/'dev'/g" api.yaml
