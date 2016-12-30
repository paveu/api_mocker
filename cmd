python src/manage.py test --test=mocker_tests --noinput --with-coverage --cover-package=mocker --cover-html --cover-erase --nologcapture --cover-html-dir=coverage_link --verbosity=0 --settings=apimocker.local_test
python manage.py runserver --settings=apimocker.dev

