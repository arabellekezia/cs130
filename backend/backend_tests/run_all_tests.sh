#!/bin/bash

python3.7 set_up_test_db.py
python3.7 test_db.py
python3.7 test_staywell.py
python3.7 test_diet.py
python3.7 test_edamam_api.py
python3.7 test_fitness.py
python3.7 test_goals.py
python3.7 test_sleep.py
python3.7 test_user.py
python3.7 drop_test_tables.py
