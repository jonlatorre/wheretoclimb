wheretoclimb
============

wheretoclimb

installation
============

Install python-mysql and libgeos-c

pip install -r requirements/project.txt

create/edit locale_settings.py

Prepare the database:

./manage.py syncdb
./manage.py loaddata foto
./manage.py loaddata grade
./manage.py loaddata crags
