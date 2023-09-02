""" main module """

import json
import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError, ValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from containers import Container
from app.api import api


def get_application(cont) -> FastAPI:
    """ application class """

    load_dotenv()

    db = cont.gateways.db()
    db.create_database()

    application = FastAPI()

    origins = ["*"]

    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    if not os.path.exists("bits"):
        os.makedirs("bits")

    application.mount("/bits", StaticFiles(directory="bits"), name="bits")

    @application.exception_handler(RequestValidationError)
    @application.exception_handler(ValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """ validation exception handler """

        exc_json = json.loads(exc.json())
        response = {"status": "fail", "data": []}
        for error in exc_json:
            response['data'].append(error['loc'][-1]+f": {error['msg']}")

        return JSONResponse(
            status_code=422,
            content=response
        )

    application.container = cont
    application.include_router(api.router)

    return application


container = Container()
app = get_application(container)
