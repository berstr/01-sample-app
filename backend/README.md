export NEW_RELIC_APP_NAME=sample-app;
export NEW_RELIC_LICENSE_KEY=<INGEST KEY>

newrelic-admin run-program uvicorn main:app --host 0.0.0.0 --port 27533 --reload  
