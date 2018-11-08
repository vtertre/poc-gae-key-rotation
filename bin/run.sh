#!/usr/bin/env bash

dev_appserver.py api.yaml \
    --port=8089 \
    --admin_port=8002 \
    --env_var GOOGLE_APPLICATION_CREDENTIALS=/Users/vincent/Downloads/sandbox-vincent-all-in-one.json