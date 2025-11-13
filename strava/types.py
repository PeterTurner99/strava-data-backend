from typing import TypedDict


class RefreshStravaAuthDict(TypedDict):
    refresh_token: str
    grant_type: str

class InitialStravaAuthDict(TypedDict):
    code:str
    grant_type: str