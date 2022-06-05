"""
Template for API response
"""

from enum import Enum
import json


class ResponseStatus(Enum):
    """
    Response status enum
    """
    SUCCESS = "SUCCESS"
    FAIL = "FAIL"
    ERROR = "ERROR"


class Response:
    """
    General API response class
    """

    def __init__(self, status: ResponseStatus, data: any = None, message: str = None):
        self.status = status
        self.data = data
        self.message = message

    def to_json(self):
        """
        Json parser
        """
        return json.dumps(
            {
                "status": self.status.name,
                "message": self.message,
                "data": self.data
            },
            default=lambda o: o.__dict__,
            indent=2
        )
