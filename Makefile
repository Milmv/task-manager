.PHONY: test test-cov test-html locust clean

test:
	pytest tests/ -v

test-cov:
	pytest tests/ --cov=. --cov-report=term-missing --cov-fail-under=90

test-html:
	pytest tests/ --cov=. --cov-report=html --cov-report=term-missing
	open htmlcov/index.html

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
