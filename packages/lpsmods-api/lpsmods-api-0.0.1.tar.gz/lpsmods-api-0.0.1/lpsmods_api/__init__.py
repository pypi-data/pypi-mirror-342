__all__ = ["LPSModsClient"]
__version__ = "0.0.1"

from typing import Optional
from requests import Session
import os

from .models import Info

try:
    import dotenv

    dotenv.load_dotenv()
except ImportError:
    ...


class LPSModsClient:
    def __init__(self, username: Optional[str] = None, password: Optional[str] = None):
        self.username = os.getenv("LPSMODS_USERNAME") if username is None else username
        self.password = os.getenv("LPSMODS_PASSWORD") if password is None else password
        self.session = Session()

    def _get(self, path: str):
        res = self.session.get("https://api.lpsmods.dev" + path)
        res.raise_for_status()
        return res.json()

    def fetch_info(self):
        return Info.model_validate(self._get(""))
