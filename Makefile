build:
	docker build -t tapo-exporter .

run:
	docker run --env-file tapo-exporter.env --publish "9877:9877" tapo-exporter
