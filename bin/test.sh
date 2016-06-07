set -e
cd ..
python manage.py makemigrations
python manage.py test
