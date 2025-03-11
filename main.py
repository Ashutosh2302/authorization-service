import certifi
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from mangum import Mangum
from mongoengine import connect

from common.exceptions.bad_request import BadRequestError, BadRequestException
from common.exceptions.not_found import NotFoundError, NotFoundException
from dotenv import load_dotenv
import os
from routers.authorization_router import authorization_router
from routers.health import health_router

load_dotenv()

connection = None


def connect_to_db():
    uri = os.getenv("MONGODB_URL")
    database_name = os.getenv("MONGODB_DB_NAME")

    global connection
    connection = connect(db=database_name, host=uri, tlsCAFile=certifi.where())
    print("connected to DB")


if connection is None:
    print("Connecting to DB")
    connect_to_db()

app = FastAPI(root_path="/api/authorization-service", title="Authorization Service")

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(authorization_router, tags=["Authorization"], prefix="/api/authorize")
app.include_router(health_router, tags=["Health"], prefix="/api")

@app.exception_handler(BadRequestException)
async def bad_request_exception_handler(request, exc: BadRequestException):
    return JSONResponse(
        status_code=400,
        content=BadRequestError(error=exc.error, message=exc.message).model_dump(),
    )


@app.exception_handler(NotFoundException)
async def not_found_exception_handler(request, exc: NotFoundException):
    return JSONResponse(
        status_code=404,
        content=NotFoundError(error=exc.error, message=exc.message).model_dump(),
    )


handler = Mangum(app)