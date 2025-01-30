ifeq ($(OS),Windows_NT)
    DOCKER_COMPOSE = docker-compose
else
    DOCKER_COMPOSE = docker compose
endif

.EXPORT_ALL_VARIABLES:

docs:
	docker compose run --rm terraform-docs markdown table . > ./docs/terraform.md

init:
	docker compose run --rm terraform init \
		-backend-config="bucket=$(TF_STATE_BUCKET)" \
		-backend-config="key=$(TF_STATE_KEY)"

format:
	docker compose run --rm terraform fmt -recursive .

test_ci:
	docker compose run --rm terraform test -json | tee test-output.log
	docker compose run --rm node-utils tftest-to-junitxml test-output.log

lint:
	docker compose run --rm tflint --recursive

clean:
	docker compose down --remove-orphans

rebuild:
	docker compose build --no-cache

apply:
	docker compose run --rm terraform apply -auto-approve

plan:
	docker compose run --rm terraform plan

destroy:
	docker compose run --rm terraform destroy -auto-approve

build_image:
	docker build ./function

bump:
	docker compose run --rm node-utils commit-and-tag-version
