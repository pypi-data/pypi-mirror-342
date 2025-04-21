"""
Test JSON transformation for lambda proxy integration response
"""

from uuid import uuid4
from datetime import date, datetime
from decimal import Decimal
from pygrestqlambda.aws.lambda_function.json_transform import json_output


def test_uuid():
    """
    Test UUIDs are transformed correctly
    """

    uid = uuid4()

    assert json_output(uid) == str(uid)


def test_datetime():
    """
    Test UUIDs are transformed correctly
    """

    now = datetime.now()

    assert json_output(now) == now.isoformat()


def test_date():
    """
    Test dates are transformed correctly
    """

    today = date.today()
    assert json_output(today) == today.isoformat()


def test_decimal():
    """
    Test decimals are transformed correctly
    """

    assert json_output(Decimal('1.0005')) == 1.0005
    assert json_output(Decimal('1.00050')) == 1.0005
