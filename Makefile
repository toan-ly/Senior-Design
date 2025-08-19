



docker-build:
	docker build -t mental-health-assistant .

docker-run:
	docker run -d -p 8000:8000 mental-health-assistant
