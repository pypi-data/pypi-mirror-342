__all__ = ["Info"]

from pydantic import BaseModel


class Info(BaseModel):
    name: str
    about: str
    version: str
    documentation: str
