from enum import Enum
from typing import List


class ExceptionsMessages(str, Enum):
    ID_NOT_FOUND = '{model} id not found'
    NOT_FOUND = '{model} not found'
    ALREADY_EXISTS = '{model} already exists with {fields}'
    INVALID_USERNAME_SIZE = 'Username must have at least 5 characters'
    INVALID_CREDENTIALS = 'Incorrect email or password'
    EXPIRED_TOKEN = 'Token expired'
    TOKEN_NOT_PROVIDED = 'Authorization token not provided'
    INVALID_TOKEN = 'Provided token is invalid'

    @classmethod
    def already_exists(cls, model: str, conflict_fields: List[str]) -> str:
        formatted_fields = ', '.join(conflict_fields)
        return cls.ALREADY_EXISTS.format(model=model, fields=formatted_fields)
