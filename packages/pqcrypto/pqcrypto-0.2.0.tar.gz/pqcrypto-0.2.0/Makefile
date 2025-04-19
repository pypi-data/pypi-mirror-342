test:
	uv run pytest tests

clean:
	rm -rf ./dist || true
	rm -rf ./build || true
	rm -rf ./pqcrypto/_kem/* || true
	rm -rf ./pqcrypto/_sign/* || true
	rm -rf ./pqcrypto/kem/* || true
	rm -rf ./pqcrypto/sign/* || true

compile:
	uv run python3 compile.py

format:
	uvx ruff format
