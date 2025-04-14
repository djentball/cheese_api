from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
import os
from dotenv import load_dotenv

load_dotenv()


class AdminAuth(AuthenticationBackend):
    def __init__(self, secret_key: str):
        super().__init__(secret_key=secret_key)
        self.valid_username = os.getenv("ADMIN_USERNAME")
        self.valid_password = os.getenv("ADMIN_PASSWORD")

    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = form.get("username")
        password = form.get("password")
        if username == self.valid_username and password == self.valid_password:
            request.session.update({"token": "authenticated"})
            return True
        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        return request.session.get("token") == "authenticated"
