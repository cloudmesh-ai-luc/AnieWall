.PHONY: help install test view clean api-demo

PYTHON ?= python

help:
	@echo "Repository development commands"
	@echo "  make install   - install the project with development and documentation dependencies"
	@echo "  make test      - run the project test suite"
	@echo "  make view      - serve the project documentation locally"
	@echo "  make api-demo  - run MVP 2 API on loopback (requires demo tokens in environment)"
	@echo "  make clean     - remove Python cache and test artifacts"

install:
	$(PYTHON) -m pip install -e ".[dev,docs]"

test:
	$(PYTHON) -m pytest tests/ -q

api-demo:
	$(PYTHON) -m uvicorn biometric_consent.api:create_demo_app --factory --host 127.0.0.1 --port 8000

view:
	$(PYTHON) -m mkdocs serve

clean:
	$(PYTHON) -c "import pathlib, shutil; [shutil.rmtree(p, ignore_errors=True) for p in pathlib.Path('.').rglob('__pycache__')]; shutil.rmtree('.pytest_cache', ignore_errors=True)"
