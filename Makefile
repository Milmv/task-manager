.PHONY: test test-cov test-html test-docker locust clean

test:
	USE_SQLITE=true pytest tests/ -v

test-cov:
	USE_SQLITE=true pytest tests/ --cov=. --cov-report=term-missing --cov-fail-under=90

test-html:
	USE_SQLITE=true pytest tests/ --cov=. --cov-report=html --cov-report=term-missing
	open htmlcov/index.html
test-docker:
	docker-compose up -d --build
	sleep 5
	docker-compose exec app pytest tests/ -v
	docker-compose down

locust:
	uvicorn main:app --port 8000 &
	sleep 3
	locust -f tests/locustfile.py --host=http://localhost:8000 --headless -u 10 -r 2 --run-time 30s --csv=locust_report
	pkill -f uvicorn
	sleep 3
	exit


clean:
	rm -rf htmlcov/
	rm -f .coverage
	rm -f *,cover
	rm -f *.csv
	rm -f test.db
	rm -rf .pytest_cache/
