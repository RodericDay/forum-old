set -e
python ../manage.py makemigrations
python ../manage.py test
