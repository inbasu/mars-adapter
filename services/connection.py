import json
from dataclasses import dataclass
from typing import Callable

from aiohttp import ClientSession


class StatusCodeValidator:

    @staticmethod
    def check(func) -> Callable:
        async def wrapper(self, url:str, *args) -> Responce:
            resp = await func(self, url, *args)
            match resp.status_code:
                case 200:
                    return resp
                case 401:
                    self.update_token()
                    return await wrapper(self, url, *args)
            return Responce(resp.status_code, "")
        return wrapper


@dataclass
class Responce:
    status_code: int
    data: str

    def json(self) -> dict:
        return json.loads(self.data)


class Client:
    def __init__(self, url: str, username: str, password: str, auth_token:str, client_id: str)-> None:
        self._session: ClientSession | None = None
        self._token = ""
        self.url = url
        self.client_id = client_id
        self._auth_token = auth_token
        self._auth_params = {
                "grant_type": "password",
                "username": username,
                "password": password,
                }

    @property
    def session(self) -> ClientSession:
        if not self._session:
            self._session = ClientSession(base_url=self.url)
        return self._session
    

    async def close(self) -> None:
        if self._session:
            await self._session.close()


    async def update_token(self) -> None:
        async with self.session as session:
            async with session.get("/", params=self._auth_params) as resp:
                self._token = await resp.json()


    @StatusCodeValidator.check
    async def get(self, url: str, params: dict) -> Responce:
        async with self.session.get(url, params=params) as resp:
            return Responce(status_code=resp.status, data=await resp.text())


    @StatusCodeValidator.check
    async def post(self, url: str, data: dict) -> Responce:
        async with self.session.post(url, data=data) as resp:
            return Responce(status_code=resp.status, data=await resp.text())


        