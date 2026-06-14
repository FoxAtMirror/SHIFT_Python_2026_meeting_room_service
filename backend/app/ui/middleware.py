from starlette.middleware.base import BaseHTTPMiddleware

from fastapi import Request
from fastapi.responses import RedirectResponse

from app.core.security import decode_access_token


class AuthMiddleware(BaseHTTPMiddleware):

    async def dispatch(
        self,
        request: Request,
        call_next
    ):

        public_paths = {
            "/",
            "/login",
            "/logout",
            "/docs",
            "/openapi.json"
        }

        if request.url.path.startswith(
            "/static"
        ):

            return await call_next(
                request
            )

        if request.url.path.startswith(
            "/api"
        ):

            return await call_next(
                request
            )

        if request.url.path in public_paths:

            return await call_next(
                request
            )

        token = request.cookies.get(
            "access_token"
        )

        if not token:

            return RedirectResponse(
                "/login",
                status_code=303
            )

        payload = decode_access_token(
            token
        )

        if not payload:

            return RedirectResponse(
                "/login",
                status_code=303
            )

        return await call_next(
            request
        )