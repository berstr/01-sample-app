from fastapi import FastAPI,  Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import PlainTextResponse
import logging
import sys
import os
import json
import requests
import random
from random import randint

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(str(os.getenv("OTEL_PYTHON_LOG_LEVEL", "INFO")).upper())

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    logger.info("http.status_text", str(exc.detail))
    logger.info(f'otel.status_description: {exc.status_code} / {str(exc.detail)}')
    return PlainTextResponse(json.dumps({ "detail" : str(exc.detail) }), status_code=exc.status_code)

@app.get("/")
def index():
    return FileResponse("./dist/index.html")

@app.get("/health")
def index():
    logger.info(f'GET /health - received')
    return { "service": "sample-app", "status": "ok" }

@app.get('/exception1')
def exception1():
    logger.info(f'GET /excpetion1 - received')
    raise HTTPException(404)
    logger.info(f'GET /excpetion1 - result 200')
    return 200

@app.get('/exception2')
def exception2():
    # logger.info(f'GET /excpetion2 - received')
    result = ''
    try:
        1/int(0)
    except:
        result = sys.exc_info()[0]
        #logger.warning(f'Excpetion: 1/int(0) occurred - {result}')
    #logger.info(f'GET /excpetion2 - result: {result}')
    return result

@app.get('/exception3')
def exception3():
    logger.info(f'GET /excpetion3 - received')
    1/int('a')
    return 200


@app.get('/status_code')
def status_code( response: Response, code: str | None = None):
    logger.info(f'GET /status_code - received - code: {code}')
    if not code:
        code = "200"
    response.status_code = int(code)
    return { "http status code": code }


@app.get("/external")
def external_api(url: str):
    logger.info(f'GET /external received - url: {url}')
    response = requests.get(url)
    response.close()
    return "ok"

# examples:
# https://httpbin.org/delay/5  -> 5 sec delay
# https://httpbin.org/status/404  -> returns with HTTP status code 404
@app.get("/httpbin")
def external_api(response: Response, action: str | None = None , value : str | None = None):
    logger.info(f'GET /httpbin received - action: {action} - value: {value}')
    if action and value:
        url = f'https://httpbin.org/{action}/{value}'
        logger.info(f'/httpbin - calling: {url} ')
        response = requests.get(url)
        response.close()
        response.status_code = 200
    else:
        logger.info(f'GET /httpbin - missing query parameter')
        response.status_code = 404

# @app.exception_handler(404)
# async def exception_404_handler(request, exc):
#    return FileResponse("./dist/index.html")

app.mount("/", StaticFiles(directory="dist", html=True), name="frontend")