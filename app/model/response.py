"""
Template for API response
"""

from enum import Enum


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

    def to_json(self) -> dict:
        """
        Parse response class to dictionary
        """
        return {
            "status": self.status.name,
            "data": self.data,
            "message": self.message
        }
