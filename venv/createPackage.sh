#!/usr/bin/env bash

mkdir endpoints-python
cd endpoints-python
pip install --target ./package pymysql
cd package
zip -r ../../endpoints-python.zip .
cd ../..
zip -g endpoints-python.zip *.py
rm -rf endpoints-python