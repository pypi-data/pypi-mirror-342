import aiohttp
from dataclasses import dataclass


@dataclass
class Credentials:
    base_url: str
    username: str
    password: str
    recaptcha: str


async def auth(credentials: Credentials) -> str:
    url = f"{credentials.base_url}/login"
    payload = {
        "username": credentials.username,
        "password": credentials.password,
        "recaptcha": credentials.recaptcha,
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as resp:
            resp.raise_for_status()
            body = await resp.text()
            return body
