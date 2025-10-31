.PHONY: help setup install start-db stop-db enrich visualize export clean test

help:
	@echo "NCII Infrastructure Mapping - Makefile Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make setup          - Create virtual environment and install dependencies"
	@echo "  make install        - Install Python dependencies"
	@echo ""
	@echo "Database:"
	@echo "  make start-db       - Start Neo4j and PostgreSQL containers"
	@echo "  make stop-db        - Stop database containers"
	@echo ""
	@echo "Processing:"
	@echo "  make enrich         - Run enrichment pipeline on domains.csv"
	@echo "  make visualize      - Start Flask visualization server"
	@echo "  make export         - Export enriched data to CSV/JSON"
	@echo ""
	@echo "Utilities:"
	@echo "  make clean          - Clean Python cache files"
	@echo "  make test           - Run tests"

setup:
	python3 -m venv venv
	. venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

install:
	pip install -r requirements.txt

start-db:
	docker-compose up -d
	@echo "Waiting for databases to be ready..."
	@sleep 5
	@echo "Databases started. Neo4j: http://localhost:7474"

stop-db:
	docker-compose down

enrich:
	python scripts/enrich_domains.py

visualize:
	python app.py

export:
	python scripts/export_data.py

clean:
	find . -type d -name __pycache__ -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

test:
	pytest tests/ -v

