from typing import Optional
from aiohttp import ClientSession, ClientError

from .consts import PARAMS, HEADERS


class HTTPClient:
    _session: Optional[ClientSession] = None

    def __init__(self):
        pass

    @property
    def session(self):
        if type(type(self)._session) is None:
            raise RuntimeError("HTTPClient session is not initialized")
        return type(self)._session

    @classmethod
    async def init(cls):
        if cls._session is None:
            cls._session = ClientSession(headers=HEADERS)

    @classmethod
    async def close(cls):
        if cls._session is not None:
            await cls._session.close()
            cls._session = None

    async def get(self,
                  url: str,
                  v_token: str = "",
                  auth_token: str = "",
                  student_name: str = "",
                  vendor: str = "",
                  days: str = ""):

        params = {
            **PARAMS,
            "v_token": v_token,
            "auth_token": auth_token,
            "student": student_name,
            "vendor": vendor,
            "days": days
        }

        async with self.session.get(url, params=params) as response:
            try:
                response.raise_for_status()
            except ClientError as exp:
                print("[ERROR] HTTPClient.get():", str(exp))
                return None
            return await response.json()


http_client = HTTPClient()
