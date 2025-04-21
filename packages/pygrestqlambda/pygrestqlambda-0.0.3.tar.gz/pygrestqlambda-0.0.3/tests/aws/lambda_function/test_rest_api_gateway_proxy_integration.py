"""
Test REST API Gateway lambda proxy integration response
"""

import base64
import json
from pygrestqlambda.aws.lambda_function.rest_api_gateway_proxy_integration import Response


def test_json_response():
    """
    Test JSON response is prepared correctly
    """

    response = Response()
    response.body = {'hello': 'world'}

    payload = response.get_payload()

    print(payload)

    assert payload['headers']['Content-Type'] == 'application/json'
    assert json.loads(payload['body'])['hello'] == 'world'


def test_binary_response():
    """
    Test binary response is correctly prepared
    """

    response = Response(
        body=b'hello world',
        is_base64_encoded=True
    )

    payload = response.get_payload()

    assert base64.b64decode(payload['body']) == b'hello world'
