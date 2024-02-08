run:
	docker-compose up -d
down:
	docker-compose down
info:
	docker ps -a

delete-services:
	docker rmi bonus_service; \
	docker rmi flight_service; \
	docker rmi ticket_service; \
	docker rmi gateway_service;

delete-all:
	docker rmi bonus_service; \
	docker rmi flight_service; \
	docker rmi ticket_service; \
	docker rmi gateway_service; \
	rm -rf pg_data_bonus; \
	rm -rf pg_data_flight; \
	rm -rf pg_data_ticket;

restart:
	docker-compose down; \
	docker rmi gateway_service; \
	docker-compose up -d

logs:
	docker logs gateway_service
	
# run-tests:
# 	pytest -vs unit_tests/flight.py

# pg_dump -U postgres flight_db > db.sql
