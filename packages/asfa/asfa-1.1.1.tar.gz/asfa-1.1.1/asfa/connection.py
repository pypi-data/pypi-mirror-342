import httpx
from ._config import get_api_url

class AuthClient:
    def __init__(self):
        self.base_url = get_api_url()

    def login(self, username: str, password: str) -> str:
        response = httpx.post(f"{self.base_url}/auth/token", data={
            "username": username,
            "password": password
        })
        response.raise_for_status()
        return response.json().get("access_token")

    def get_me(self, token: str):
        return self._get("/users/me", token)

    def _get(self, path: str, token: str):
        response = httpx.get(
            f"{self.base_url}{path}",
            headers={"Authorization": f"Bearer {token}"}
        )
        response.raise_for_status()
        return response.json()
