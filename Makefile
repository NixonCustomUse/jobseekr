.PHONY: test test-v run seed clean

test:
	python3 -m pytest tests -v --tb=short

test-v:
	python3 -m pytest tests -v --tb=long

run:
	cd backend && python3 app.py

seed:
	cd backend && python3 seed.py

clean:
	rm -f backend/data.db backend/data.db-shm backend/data.db-wal
	rm -rf backend/__pycache__ backend/.pytest_cache
	rm -rf tests/__pycache__
