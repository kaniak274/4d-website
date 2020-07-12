#!/bin/sh

set -e

MANAGE_PY=/app/manage.py
REQUIREMENTS=/app/requirements/base.txt

pip3 install -r $REQUIREMENTS
npm install
$MANAGE_PY migrate
npm run dev
