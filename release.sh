#!/bin/bash

flask db upgrade
cd ./frontend && npm run-script build
