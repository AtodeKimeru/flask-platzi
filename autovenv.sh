#!/bin/bash

source venv/bin/activate
pip install -r requirements.txt

export FLASK_APP=main.py
export FLASK_DEBUG=1

echo 'flask run to start app'