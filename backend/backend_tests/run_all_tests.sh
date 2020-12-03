#!/bin/bash

/usr/local/bin/python3 set_up_test_db.py
coverage run --source=../../backend -m unittest discover tests
coverage report -m
/usr/local/bin/python3 drop_test_tables.py
