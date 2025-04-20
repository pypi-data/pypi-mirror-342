from fastapi import Request
from fastapi.responses import HTMLResponse

from starlette.middleware.base import BaseHTTPMiddleware


class PermissionMiddleware:
    def __init__(self, app):
        self.app = app  # Сохраняем приложение FastAPI

    async def __call__(self, scope, receive, send):
        # Проверяем, что это HTTP-запрос
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        # Создаем объект Request для удобства работы
        request = Request(scope, receive)

        # Проверяем, авторизован ли пользователь
        if not hasattr(request, "user") or not getattr(request.user, "is_authenticated", False):
            response = HTMLResponse('Forbidden', status_code=403)
            await response(scope, receive, send)
            return

        # Проверяем соответствие display_name и user_id из path_params
        if request.user.display_name == request.path_params.get('user_id'):
            # Если проверка прошла, передаем управление дальше
            await self.app(scope, receive, send)
            return

        # Если проверка не прошла, возвращаем ошибку 403
        response = HTMLResponse('Forbidden', status_code=403)
        await response(scope, receive, send)
