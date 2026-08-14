
from pydantic import BaseModel


class APIRequest(BaseModel):

    method: str

    path: str

    body: dict | None = None