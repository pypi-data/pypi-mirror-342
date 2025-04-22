import asyncio
import fastapi.openapi.utils as fu
import uvloop

from ctesiphon.dto.base import BaseError
from fastapi import FastAPI, APIRouter, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from hypercorn.asyncio import serve
from hypercorn.config import Config


async def token_extension(request: Request, call_next):
    access_token: str | None = request.headers.get("x-access-token", None)

    request.state.access_token = access_token
    response = await call_next(request)

    return response


class CtesiphonFastAPIService:
    def __init__(self,
            container: any,
            title: str,
            version: str,
            root_path: str,
            debug: bool,
            routers: list[tuple[str, APIRouter]],
            bind_host: str,
        ):
        self.container = container
        self.app = FastAPI(
            title=title,
            version=version,
            docs_url="/api-docs" if debug else None,
            redoc_url=None,
            root_path=root_path,
            debug=debug,
        )
        self.app.container = container
        for router in routers:
            self.app.include_router(router[1], prefix=router[0])
        
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        self.app.middleware("http")(token_extension)

        @self.app.exception_handler(RequestValidationError)
        async def validation_exception_handler(request, exc):
            return JSONResponse({"error": "Validation error!"}, status_code=422)
        
        @self.app.exception_handler(BaseError)
        async def base_exception_handler(request, exc: BaseError):
            return JSONResponse({
                "error": exc.description,
                "code": exc.error_code,
                "http_status": exc.http_status,
            }, status_code=exc.http_status)


        fu.validation_error_response_definition = {
            "title": "HTTPValidationError",
            "type": "object",
            "properties": {
                "error": {"title": "Message", "type": "string"}, 
            },
        }

        self.hypercorn_config = Config()
        self.hypercorn_config.bind = [ bind_host ]

    def run(self):
        uvloop.install()
        asyncio.run((serve(self.app, self.hypercorn_config)))
