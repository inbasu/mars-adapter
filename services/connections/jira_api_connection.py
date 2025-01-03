from services.connections.connection import Client, Responce


class JiraAPIClient(Client):
    url = "https://jira.metro-cc.ru/rest/api/2/"

    def __init__(self, username: str, password: str) -> None:
        self._auth = (username, password)

    async def get(self, url: str, params: dict) -> Responce:
        resp = await self.session.get(url=url, params=params, auth=self._auth)
        return Responce(resp.status_code, resp.json())

    async def post(self, url, *args, **kwargs) -> Responce:
        pass
