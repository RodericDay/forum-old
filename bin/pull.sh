scp roderic@projects.roderic.ca:forum/db.sqlite3 ..
python ../manage.py migrate
python ../manage.py dumpdata posts auth > ../dump.json
