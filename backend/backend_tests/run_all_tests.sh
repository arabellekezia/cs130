#!/bin/bash

python3.7 set_up_test_db.py
coverage run --source=../../backend --omit=*test_*,*app* -m unittest discover tests
coverage report -m
python3.7 drop_test_tables.py
