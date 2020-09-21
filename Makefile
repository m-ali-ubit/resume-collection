up:
	docker-compose -f local.yml up

upnew:
	docker-compose -f local.yml build
	docker-compose -f local.yml up -d django
	docker exec django ../entrypoint python manage.py makemigrations
	docker exec django ../entrypoint python manage.py migrate
	docker-compose -f local.yml down

migrate:
	docker exec -it django ../entrypoint python manage.py migrate

migrations:
	docker exec -it django ../entrypoint python manage.py makemigrations

superuser:
	docker exec -it django ../entrypoint python manage.py createsuperuser

djangoshell:
	docker exec -it django ../entrypoint python manage.py shell

shell:
	docker exec -it django ../entrypoint /bin/sh
