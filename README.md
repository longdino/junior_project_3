# eh-DSS
DSS for Engineering Honors


Install needed packages and create virtual env.
>pipenv install

This will update your pipenv environment to the lock file contents. Run if you already have a pipenv established.
>pipenv sync

Activate virtual env.
>pipenv shell

Create db migrations then create db off that schema.
>python manage.py makemigrations\
>python manage.py migrate

Test. Creates test db from migration and deletes said db after testing.
>python manage.py test

To generate coverage for eh_app, run tests with coverage and view generated report. -m shows line number for statements missing tests.
>coverage run --source='./eh_app' manage.py test\
>coverage report -m

Various commands for loading test data, config data, cleaning migrations can be found in the make file. The following will delete the current db, rebuild migrations, migrate, and load config data for the dev db:
>make clean_dev_db_to_config

Get out of virtual env.
>exit

If you're doing mysql connections on Windows, download mysqlclient-1.4.2-cp37-cp37m-win32.whl from 
https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient, move it into EH-DSS/ (parent directory) and then run
>pip install mysqlclient-1.4.2-cp37-cp37m-win32.whl
