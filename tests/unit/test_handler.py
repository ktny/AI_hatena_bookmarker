import json

import pytest

from src import app


@pytest.fixture()
def apigw_event():
    """Generates API GW Event"""

    return {
        "resource": "/hello",
        "path": "/hello",
        "httpMethod": "GET",
        "requestContext": {"Dummy": "Dummy"},
    }


def test_lambda_handler(apigw_event, mocker):

    ret = app.lambda_handler(apigw_event, "")
    data = json.loads(ret["body"])

    assert ret["statusCode"] == 200
    assert "message" in ret["body"]
    assert data["message"] == "Hello World"
