from _typeshed import Incomplete
from fastapi import Request
from fastapi.staticfiles import StaticFiles

security: Incomplete

async def verify_username(request: Request) -> str: ...

class AuthStaticFiles(StaticFiles):
    def __init__(self, *args, **kwargs) -> None: ...
    async def __call__(self, scope, receive, send) -> None: ...
