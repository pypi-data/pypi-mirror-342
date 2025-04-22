import aiohttp
from dataclasses import dataclass


@dataclass
class Upload:
    base_url: str
    token: str
    folder: str
    filename: str
    shared_url: str


async def delete_file(upload: Upload) -> None:
    url = f"{upload.base_url}/resources/{upload.folder}/{upload.filename}"
    headers = {"X-Auth": upload.token}

    async with aiohttp.ClientSession() as session:
        async with session.delete(url, headers=headers) as resp:
            if resp.status != 204:
                raise Exception(f"File not found: {url} (status: {resp.status})")


async def create_empty_file(upload: Upload) -> str:
    url = f"{upload.base_url}/tus/{upload.folder}/{upload.filename}?override=false"
    headers = {"X-Auth": upload.token}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers) as resp:
            if resp.status not in (200, 201):
                raise Exception(f"Failed to create empty file: {url} (status: {resp.status})")

    share_url = f"{upload.base_url}/{upload.shared_url}/{upload.filename}?inline=true"
    return share_url


async def fill_empty_file(upload: Upload, file_bytes: bytes, override: bool = False) -> None:
    url = f"{upload.base_url}/tus/{upload.folder}/{upload.filename}?override={str(override).lower()}"

    headers = {
        "X-Auth": upload.token,
        "Content-Type": "application/offset+octet-stream",
        "Content-Length": str(len(file_bytes)),
        "Upload-Offset": "0"
    }

    cookies = {
        "auth": upload.token
    }

    async with aiohttp.ClientSession(cookies=cookies) as session:
        async with session.patch(url, data=file_bytes, headers=headers) as resp:
            if resp.status not in (200, 204):
                raise Exception(f"Failed to fill empty file: {url} (status: {resp.status})")


async def upload(upload: Upload, file_bytes: bytes) -> str:
    try:
        share_url = await create_empty_file(upload)
    except Exception as e:
        raise Exception(f"Error creating empty file: {e}")

    try:
        await fill_empty_file(upload, file_bytes)
    except Exception as e:
        raise Exception(f"Error filling file: {e}")

    return share_url
