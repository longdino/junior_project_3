load_config:
	python manage.py loaddata eh_app/fixtures/Department.yaml
	python manage.py loaddata eh_app/fixtures/EmailTemplate.yaml
	python manage.py loaddata eh_app/fixtures/Exception.yaml
	python manage.py loaddata eh_app/fixtures/GPAandPartDef.yaml
	python manage.py loaddata eh_app/fixtures/GPADefAndStatus.yaml
	python manage.py loaddata eh_app/fixtures/HonorsCreditsRating.yaml
	python manage.py loaddata eh_app/fixtures/ParticipationStatus.yaml
	python manage.py loaddata eh_app/fixtures/ProbandGPADef.yaml
	python manage.py loaddata eh_app/fixtures/ProbDefStatus.yaml
	python manage.py loaddata eh_app/fixtures/Requirement.yaml
	python manage.py loaddata eh_app/fixtures/Tracks.yaml

	python manage.py loaddata eh_app/fixtures/others.yaml

	python manage.py import_exception_values_csv
load_seed:
	python manage.py loaddata eh_app/fixtures/test_seed.yaml
clean_migrations:
	find eh_app/migrations ! -name '__init__.py' -type f -exec rm -f {} +
make_migrate:
	python manage.py makemigrations && python manage.py migrate
rm_dev_db:
	-rm db.sqlite3
clean_dev_db_to_config:
	$(MAKE) rm_dev_db
	$(MAKE) clean_migrations
	$(MAKE) make_migrate
	$(MAKE) load_config
