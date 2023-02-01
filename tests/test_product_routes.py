from http import HTTPStatus
from typing import Dict

import pytest
from flask import Flask
from flask.testing import FlaskClient


@pytest.mark.parametrize(
    "test_products",
    [
        {"product_name": "apple", "price": 100},
        {"product_name": "orange", "price": 404},
    ],
)
def test_product_creation(app: Flask, client: FlaskClient, test_products: Dict) -> None:
    product_name = test_products["product_name"]
    price = test_products["price"]
    response = client.post(
        "/product/create",
        data={"product_name": product_name, "price": price},
    )
    assert int(response.status.split()[0]) == HTTPStatus.CREATED.numerator


@pytest.mark.parametrize(
    "test_products",
    [
        {"product_name": "apple", "price": "hello"},
        {"name": "product_name", "price": 55.55},
        {"this should return 400": "400"},
        {},
        {500: 500},
    ],
)
def test_bad_product_creation(app: Flask, client: FlaskClient, test_products: Dict) -> None:
    product_name = test_products["product_name"]
    price = test_products["price"]
    response = client.post(
        "/product/create",
        data={"product_name": product_name, "price": price},
    )
    assert int(response.status.split()[0]) == HTTPStatus.BAD_REQUEST.numerator
