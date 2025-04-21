#!/usr/bin/env python3

__author__ = "xi"
__all__ = [
    "MCPMethod",
]

import asyncio
import traceback
from inspect import signature
from types import GeneratorType
from typing import Callable, Dict, Iterable, Optional, Type, Union

from flask import Flask, request as flask_request
from pydantic import BaseModel

from libentry import api, json, logger
from libentry.api import list_api_info
from libentry.schema import query_api

try:
    from gunicorn.app.base import BaseApplication
except ImportError:
    class BaseApplication:

        def load(self) -> Flask:
            pass

        def run(self):
            flask_server = self.load()
            assert hasattr(self, "options")
            bind = getattr(self, "options")["bind"]
            pos = bind.rfind(":")
            host = bind[:pos]
            port = int(bind[pos + 1:])
            logger.warn("Your system doesn't support gunicorn.")
            logger.warn("Use Flask directly.")
            logger.warn("Options like \"num_threads\", \"num_workers\" are ignored.")
            return flask_server.run(host=host, port=port)


class MCPMethod:

    def __init__(self, fn: Callable, method: str = None):
        self.fn = fn
        assert hasattr(fn, "__name__")
        self.__name__ = fn.__name__
        self.method = self.__name__ if method is None else method

        self.input_schema = None
        params = signature(fn).parameters
        if len(params) == 1:
            for name, value in params.items():
                annotation = value.annotation
                if isinstance(annotation, type) and issubclass(annotation, BaseModel):
                    self.input_schema = annotation

    def __call__(self, request: dict) -> Union[dict, Iterable[dict]]:
        try:
            jsonrpc_version = request["jsonrpc"]
            request_id = request["id"]
            method = request["method"]
        except KeyError:
            raise RuntimeError("Invalid JSON-RPC specification.")

        if not isinstance(request_id, (str, int)):
            raise RuntimeError(
                f"Request ID should be an integer or string. "
                f"Got {type(request_id)}."
            )

        if method != self.method:
            raise RuntimeError(
                f"Method missmatch."
                f"Expect {self.method}, got {method}."
            )

        params = request.get("params", {})

        try:
            if self.input_schema is not None:
                # Note that "input_schema is not None" means:
                # (1) The function has only one argument;
                # (2) The arguments is a BaseModel.
                # In this case, the request data can be directly validated as a "BaseModel" and
                # subsequently passed to the function as a single object.
                pydantic_params = self.input_schema.model_validate(params)
                result = self.fn(pydantic_params)
            else:
                # The function has multiple arguments, and the request data bundle them as a single object.
                # So, they should be unpacked before pass to the function.
                result = self.fn(**params)
        except Exception as e:
            if isinstance(e, (SystemExit, KeyboardInterrupt)):
                raise e
            return {
                "jsonrpc": jsonrpc_version,
                "id": request_id,
                "error": self._make_error(e)
            }

        if not isinstance(result, (GeneratorType, range)):
            return {
                "jsonrpc": jsonrpc_version,
                "id": request_id,
                "result": result
            }

        return ({
            "jsonrpc": jsonrpc_version,
            "id": request_id,
            "result": item
        } for item in result)

    @staticmethod
    def _make_error(e):
        err_cls = e.__class__
        err_name = err_cls.__name__
        module = err_cls.__module__
        if module != "builtins":
            err_name = f"{module}.{err_name}"
        return {
            "code": 1,
            "message": f"{err_name}: {str(e)}",
            "data": traceback.format_exc()
        }


class FlaskMethod:

    def __init__(self, method, api_info, app):
        self.method = MCPMethod(method)
        self.api_info = api_info
        self.app = app
        assert hasattr(method, "__name__")
        self.__name__ = method.__name__

    CONTENT_TYPE_JSON = "application/json"
    CONTENT_TYPE_SSE = "text/event-stream"

    def __call__(self):
        args = flask_request.args
        data = flask_request.data
        content_type = flask_request.content_type
        accepts = flask_request.accept_mimetypes

        json_from_url = {**args}
        if data:
            if (not content_type) or content_type == self.CONTENT_TYPE_JSON:
                json_from_data = json.loads(data)
            else:
                return self.app.error(f"Unsupported Content-Type: \"{content_type}\".")
        else:
            json_from_data = {}

        conflicts = json_from_url.keys() & json_from_data.keys()
        if len(conflicts) > 0:
            return self.app.error(f"Duplicated fields: \"{conflicts}\".")

        input_json = {**json_from_url, **json_from_data}
        print(input_json)

        try:
            output_json = self.method(input_json)
        except Exception as e:
            return self.app.error(str(e))

        if isinstance(output_json, Dict):
            if self.CONTENT_TYPE_JSON in accepts:
                return self.app.ok(json.dumps(output_json), mimetype=self.CONTENT_TYPE_JSON)
            else:
                return self.app.error(f"Unsupported Accept: \"{[*accepts]}\".")
        elif isinstance(output_json, (GeneratorType, range)):
            if self.CONTENT_TYPE_SSE in accepts:
                # todo
                return self.app.ok(json.dumps(output_json), mimetype=self.CONTENT_TYPE_SSE)
            else:
                return self.app.error(f"Unsupported Accept: \"{[*accepts]}\".")


class FlaskServer(Flask):

    def __init__(self, service):
        super().__init__(__name__)
        self.service = service

        logger.info("Initializing Flask application.")
        self.api_info_list = list_api_info(service)
        if len(self.api_info_list) == 0:
            logger.error("No API found, nothing to serve.")
            return

        for fn, api_info in self.api_info_list:
            method = api_info.method
            path = api_info.path
            if asyncio.iscoroutinefunction(fn):
                logger.error(f"Async function \"{fn.__name__}\" is not supported.")
                continue
            logger.info(f"Serving {method}-API for {path}")

            wrapped_fn = FlaskMethod(fn, api_info, self)
            if method == "GET":
                self.get(path)(wrapped_fn)
            elif method == "POST":
                self.post(path)(wrapped_fn)
            else:
                raise RuntimeError(f"Unsupported method \"{method}\" for ")

        for fn, api_info in list_api_info(self):
            method = api_info.method
            path = api_info.path

            if any(api_info.path == a.path for _, a in self.api_info_list):
                logger.info(f"Use custom implementation of {path}.")
                continue

            if asyncio.iscoroutinefunction(fn):
                logger.error(f"Async function \"{fn.__name__}\" is not supported.")
                continue
            logger.info(f"Serving {method}-API for {path}")

            wrapped_fn = FlaskMethod(fn, api_info, self)
            if method == "GET":
                self.get(path)(wrapped_fn)
            elif method == "POST":
                self.post(path)(wrapped_fn)
            else:
                raise RuntimeError(f"Unsupported method \"{method}\" for ")

        logger.info("Flask application initialized.")

    @api.get("/")
    def index(self, name: str = None):
        if name is None:
            all_api = []
            for _, api_info in self.api_info_list:
                all_api.append({"path": api_info.path})
            return all_api

        for fn, api_info in self.api_info_list:
            if api_info.path == "/" + name:
                return query_api(fn).model_dump()

        return f"No API named \"{name}\""

    @api.get()
    def live(self):
        return "OK"

    def ok(self, body: Union[str, Iterable[str]], mimetype: str):
        return self.response_class(body, status=200, mimetype=mimetype)

    def error(self, body: str, mimetype="text"):
        return self.response_class(body, status=500, mimetype=mimetype)


class GunicornApplication(BaseApplication):

    def __init__(self, service_type, service_config=None, options=None):
        self.service_type = service_type
        self.service_config = service_config
        self.options = options or {}
        super().__init__()

    def load_config(self):
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        logger.info("Initializing the service.")
        if isinstance(self.service_type, type) or callable(self.service_type):
            service = self.service_type(self.service_config) if self.service_config else self.service_type()
        elif self.service_config is None:
            logger.warning(
                "Be careful! It is not recommended to start the server from a service instance. "
                "Use service_type and service_config instead."
            )
            service = self.service_type
        else:
            raise TypeError(f"Invalid service type \"{type(self.service_type)}\".")
        logger.info("Service initialized.")

        return FlaskServer(service)


def run_service(
        service_type: Union[Type, Callable],
        service_config=None,
        host: str = "0.0.0.0",
        port: int = 8888,
        num_workers: int = 1,
        num_threads: int = 20,
        num_connections: Optional[int] = 1000,
        backlog: Optional[int] = 1000,
        worker_class: str = "gthread",
        timeout: int = 60,
        keyfile: Optional[str] = None,
        keyfile_password: Optional[str] = None,
        certfile: Optional[str] = None
):
    logger.info("Starting gunicorn server.")
    if num_connections is None or num_connections < num_threads * 2:
        num_connections = num_threads * 2
    if backlog is None or backlog < num_threads * 2:
        backlog = num_threads * 2

    def ssl_context(config, default_ssl_context_factory):
        import ssl
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(
            certfile=config.certfile,
            keyfile=config.keyfile,
            password=keyfile_password
        )
        context.minimum_version = ssl.TLSVersion.TLSv1_3
        return context

    options = {
        "bind": f"{host}:{port}",
        "workers": num_workers,
        "threads": num_threads,
        "timeout": timeout,
        "worker_connections": num_connections,
        "backlog": backlog,
        "keyfile": keyfile,
        "certfile": certfile,
        "worker_class": worker_class,
        "ssl_context": ssl_context
    }
    for name, value in options.items():
        logger.info(f"Option {name}: {value}")
    GunicornApplication(service_type, service_config, options).run()
