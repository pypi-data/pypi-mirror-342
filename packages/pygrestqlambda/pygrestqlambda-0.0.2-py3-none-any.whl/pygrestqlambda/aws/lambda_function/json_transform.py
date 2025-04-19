"""
JSON output transformer for non-serialisable values
"""

from uuid import UUID
from datetime import datetime


def json_output(value: object) -> str:
    """
    Calculates the serialised version of an object to return in a JSON response
    """

    # Handle UUIDs
    if isinstance(value, UUID):
        value = str(value)

    # Handle timestamps
    if isinstance(value, datetime):
        value = value.isoformat()

    return value
