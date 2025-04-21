all: schema models

.PHONY: install
install:
	npm i && uv sync

.PHONY: check
check:
	@npx tsc index.mts --noEmit

.PHONY: schema
schema:
	@npx typescript-json-schema \
		--titles \
		--refs --topRef --aliasRef \
		--propOrder --excludePrivate \
		--strictNullChecks \
		index.mts Dashboard > generated/schema.json

models:
	@uvx --from datamodel-code-generator datamodel-codegen \
		--input generated/schema.json \
		--input-file-type jsonschema \
		--output generated/models.py \
		--output-model-type dataclasses.dataclass \
		--use-generic-container-types \
		--use-standard-collections \
		--enum-field-as-literal all \
		--use-union-operator \
		--reuse-model \
		--use-schema-description \
		--use-field-description \
		--use-title-as-name \
		--formatters ruff-format

build:
	@uv build
