# Project

#How to Contribute

0. Create virtual environment with python v3.6 (https://virtualenv.pypa.io/en/latest/)

1. clone this repositories
2. create database
3. add database settengs to `settings.py`
4. install requirements: 'pip install -r requirements.txt`
5. run migration `python manage.py migrate`
6. create admin user `python manage.py createsuperuser`
7. run dev server