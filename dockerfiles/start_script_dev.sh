#!/bin/sh

python manage.py migrate --no-input
python manage.py loaddata json_data/group_data.json
python manage.py loaddata json_data/employee_category.json
python manage.py loaddata json_data/account_data.json
python manage.py loaddata json_data/main_data.json
python manage.py loaddata json_data/review_data.json
python manage.py loaddata blog_data_latest.json

