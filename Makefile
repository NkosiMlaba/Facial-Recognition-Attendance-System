
WEBAPI_JAR_FILE = target/facial-recognition-attendance-system-1.0-SNAPSHOT-webapi-jar-with-dependencies.jar

.PHONY: all
all: clean build setup-venv install-dependencies

.PHONY: clean
clean:
	mvn clean

.PHONY: build
build:
	mvn package

.PHONY: build-no-tests
build-no-tests:
	mvn package -DskipTests

.PHONY: tests
tests:
	mvn test

.PHONY: webapi
webapi: build
	java -jar $(WEBAPI_JAR_FILE)

.PHONY: run-webapi
run-webapi: 
	java -jar $(WEBAPI_JAR_FILE)

.PHONY: push
push:
	@read -p "Enter commit message: " msg; \
	git add .; \
	git commit -m "$$msg"; \
	git push

.PHONY: setup-venv
setup-venv:
	@echo "Setting up virtual environment..."
	@if [ "$(OS)" = "Windows_NT" ]; then \
		python -m venv .venv; \
		.venv\\Scripts\\activate; \
		python -m pip install --upgrade pip; \
	else \
		python3 -m venv .venv; \
		. .venv/bin/activate; \
	fi

.PHONY: install-dependencies
install-dependencies: setup-venv
	@echo "Installing dependencies..."
	@if [ "$(OS)" = "Windows_NT" ]; then \
		.venv\\Scripts\\activate && pip install -r dependencies/requirements.txt; \
	else \
		. .venv/bin/activate && pip install -r dependencies/requirements.txt; \
	fi