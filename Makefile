dev:
	uv run services/${service}/src/${service}/main.py

push:
#This command loads the Docker image into the kind cluster, in actual setting this should be uploaded to git registry
#and then the deployment should pull the image from there.
	kind load docker-image ${service}:dev --name rwml-34fa

build:
## Create a docker image for the service
# The image is tagged as dev, which indicates that it is a development version.
# 
	docker build -t ${service}:dev -f docker/${service}.Dockerfile   .

deploy: build push
	kubectl delete -f deployments/dev/${service}/${service}.yaml --ignore-not-found=true
	kubectl apply -f deployments/dev/${service}/${service}.yaml


lint:
	ruff check . --fix

delete: 
	kubectl delete -f deployments/dev/${service}/${service}.yaml --ignore-not-found=true