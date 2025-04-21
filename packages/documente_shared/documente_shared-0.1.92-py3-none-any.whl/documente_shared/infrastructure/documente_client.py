from requests import Session
from dataclasses import dataclass
from typing import Optional


@dataclass
class DocumenteClientMixin(object):
    api_url: str
    api_key: str
    session: Optional[Session] = None

    def __post_init__(self):
        self.session = Session()
        self.session.headers.update(self.get_common_headers())


    def get_common_headers(self) -> dict:
        return {
            "X-Api-Key": self.api_key,
            "Content-Type": "application/json"
        }
        