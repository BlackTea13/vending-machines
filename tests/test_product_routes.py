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
    assert response.json["product_name"] == product_name
    assert response.json["price"] == price


@pytest.mark.parametrize(
    "test_products",
    [
        {"product_name": "", "price": -100},
        {"product_name": "bad", "price": "price"},
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


def test_view_all(app: Flask, client: FlaskClient) -> None:
    response = client.get(
        "/product/all",
    )
    assert int(response.status.split()[0]) == HTTPStatus.OK.numerator


def test_view_by_name(app: Flask, client: FlaskClient) -> None:
    response = client.get("/product/", query_string={"product_name": "coke"})
    assert int(response.status.split()[0]) == HTTPStatus.OK.numerator


def test_view_by_id(app: Flask, client: FlaskClient) -> None:
    response = client.get("/product/", query_string={"product_id": 5})
    assert response.json["product_id"] == 5
    assert response.json["product_name"] == "nail clippers"
    assert response.json["price"] == "800.12"

    response = client.get("/product/", query_string={"product_name": "nail clippers"})
    assert response.json["product_id"] == 5
    assert response.json["price"] == "800.12"


@pytest.mark.parametrize(
    "test_strings",
    [
        {"key": "product", "item": 500},
        {"key": "", "item": ""},
    ],
)
def test_bad_view_by_id(app: Flask, client: FlaskClient, test_strings: Dict) -> None:
    response = client.get("/product/", query_string={test_strings["key"]: test_strings["item"]})
    assert int(response.status.split()[0]) == HTTPStatus.BAD_REQUEST.numerator


@pytest.mark.parametrize(
    "products",
    [
        {"product_id": 1, "product_name": "pepsi", "price": "20.0"},
        {"product_id": 2, "product_name": "taro", "price": "500.0"},
    ],
)
def test_edit_product(app: Flask, client: FlaskClient, products: Dict) -> None:
    response = client.post(
        "/product/edit",
        data={
            "product_id": products.get("product_id"),
            "product_name": products.get("product_name"),
            "price": products.get("price"),
        },
    )
    assert str(response.json["product_name"]) == products.get("product_name")
    assert str(response.json["price"]) == products.get("price")


def test_edit_product_by_single_key(app: Flask, client: FlaskClient) -> None:
    response = client.post("/product/edit", data={"product_id": 1, "price": "999.0"})
    assert str(response.json["product_name"]) == "pepsi"
    assert str(response.json["price"]) == "999.0"

    response = client.post("/product/edit", data={"product_id": 1, "product_name": "orang"})
    assert str(response.json["product_name"]) == "orang"
    assert str(response.json["price"]) == "999.00"


def test_bad_edit(app: Flask, client: FlaskClient):
    response = client.post("/product/edit", data={"product_id": 1, "price": "hello"})
    assert int(response.status.split()[0]) == HTTPStatus.BAD_REQUEST.numerator


@pytest.mark.parametrize("test_products", [{"product_id": 1}, {"product_id": 2}])
def test_delete_product(app: Flask, client: FlaskClient, test_products: Dict) -> None:
    product_id = test_products.get("product_id")
    response = client.post("/product/delete", data={"product_id": product_id})
    assert int(response.status.split()[0]) == HTTPStatus.OK.numerator


def test_bad_delete_product(app: Flask, client: FlaskClient) -> None:
    response = client.post("/product/delete", data={})
    assert int(response.status.split()[0]) == HTTPStatus.BAD_REQUEST.numerator

    response = client.post("/product/delete", data={"yo": 50})
    assert int(response.status.split()[0]) == HTTPStatus.BAD_REQUEST.numerator

    response = client.post("/product/delete", data={"product_id": "hye"})
    assert int(response.status.split()[0]) == HTTPStatus.BAD_REQUEST.numerator
