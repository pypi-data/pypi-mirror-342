import asyncio
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse
import uvicorn
from studlis.webserv import staticrequest
from studlis.webserv.staticrequest import router as static_router

from studlis.webserv.pagerequest import router as dynamic_router
import os
fastapi_app = FastAPI()

class server:
    def __init__(self,main, host="127.0.0.1",port=8000):
        self.parent=main
        self.host=host
        self.port=port
        self.dev=False
        from .webserv.staticrequest import disable_cache as static_router_cache_policy
        static_router_cache_policy=main.dev # disable cache in dev mode
    async def start(self):
        """
        Starts the Uvicorn server hosting the FastAPI application asynchronously.

        This method sets up the server configuration using the specified host, port, and log level,
        and then starts the server in a non-blocking manner by scheduling it as a task in the
        asyncio event loop. This allows the FastAPI application to run concurrently with other
        asyncio tasks.

        Note:
            The server is started as an asyncio task, which means this method returns immediately
            after launching the server. The actual server operation (accepting and processing requests)
            happens in the background, managed by the asyncio event loop.

        """
       
        config = uvicorn.Config(fastapi_app, host=self.host,port=self.port,log_level="info",reload=self.dev,reload_dirs=[os.path.dirname(os.path.abspath(__file__))])
        self.uvicorn_server = uvicorn.Server(config)
        loop = asyncio.get_running_loop()
        loop.create_task(self.uvicorn_server.serve())


    async def stop(self):
        await self.uvicorn_server.shutdown()
    def include_router(self,router):fastapi_app.include_router(router)

    
# include default routers

fastapi_app.include_router(static_router)
fastapi_app.include_router(dynamic_router)


