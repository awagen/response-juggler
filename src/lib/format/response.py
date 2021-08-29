from enum import Enum


class Status(Enum):
    ERROR = 1
    OK = 2
    DENIED = 3


class Response:

    def __init__(self, status: Status, msg: str, data: dict):
        self.status = status.name
        self.msg = msg
        self.data = data
