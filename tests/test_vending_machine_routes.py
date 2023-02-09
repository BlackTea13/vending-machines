from http import HTTPStatus
from typing import Dict

import pytest
from flask import Flask
from flask.testing import FlaskClient


def test_view_all_machine(app: Flask, client: FlaskClient) -> None:
    response = client.get(
        "/vending-machine/all",
    )
    print(response.status, response.json, response.data)
    assert int(response.status.split()[0]) == HTTPStatus.OK.numerator


def test_view_machine_by_id(app: Flask, client: FlaskClient) -> None:
    response = client.get("/vending-machine/", query_string={"machine_id": 1})
    assert int(response.status.split()[0]) == HTTPStatus.OK.numerator
    assert response.json["machine_id"] == 1
    assert response.json["location"] == "front of school"


def test_view_machine_by_location(app: Flask, client: FlaskClient) -> None:
    response = client.get("/vending-machine/", query_string={"location": "front of school"})
    assert int(response.status.split()[0]) == HTTPStatus.OK.numerator
    assert response.json["machine_id"] == 1
    assert response.json["location"] == "front of school"
    response = client.get("/vending-machine/", query_string={"location": "back of school"})
    assert int(response.status.split()[0]) == HTTPStatus.OK.numerator
    assert response.json["machine_id"] == 2
    assert response.json["location"] == "back of school"


def test_bad_view_machine(app: Flask, client: FlaskClient) -> None:
    response = client.get("/vending-machine/", query_string={})
    assert int(response.status.split()[0]) == HTTPStatus.BAD_REQUEST.numerator

    response = client.get("/vending-machine/", query_string={"machine_id": "you like jazz?"})
    assert int(response.status.split()[0]) == HTTPStatus.NOT_FOUND.numerator

    response = client.get("/vending-machine/", query_string={"location": "you like jazz?"})
    assert int(response.status.split()[0]) == HTTPStatus.NOT_FOUND.numerator


@pytest.mark.parametrize("locations", [{"location": "apple"}, {"location": "new york"}])
def test_create_machine(app: Flask, client: FlaskClient, locations: Dict) -> None:
    response = client.post("/vending-machine/create/", data={"location": locations["location"]})
    assert int(response.status.split()[0]) == HTTPStatus.CREATED.numerator
    assert response.json["location"] == locations["location"]


def test_bad_create_machine(app: Flask, client: FlaskClient) -> None:
    response = client.post("/vending-machine/create/", data={})
    assert int(response.status.split()[0]) == HTTPStatus.BAD_REQUEST.numerator

    response = client.post("/vending-machine/create/", data={"location": "front of school"})
    assert int(response.status.split()[0]) == HTTPStatus.BAD_REQUEST.numerator
    assert response.data.decode() == "vending machine at that location already exists"


@pytest.mark.parametrize(
    "form_data",
    [
        {"machine_id": 3, "product_id": 3, "quantity": 35},
    ],
)
def test_add_product_to_machine(app: Flask, client: FlaskClient, form_data: Dict) -> None:
    response = client.post(
        "/vending-machine/add-product/",
        data={
            "machine_id": form_data["machine_id"],
            "product_id": form_data["product_id"],
            "quantity": form_data["quantity"],
        },
    )

    print(response.status, response.data, response.json)
    assert int(response.status.split()[0]) == HTTPStatus.OK.numerator
    assert response.data.decode() == "product successfully added"

    response = client.get("/vending-machine/", query_string={"machine_id": 3})
    for product in response.json["products"]:
        assert product["product_id"] == form_data["product_id"]


def test_bad_add_product_to_machine(app: Flask, client: FlaskClient) -> None:
    response = client.post("/vending-machine/add-product/", data={"machine_id": -100})
    assert int(response.status.split()[0]) == HTTPStatus.BAD_REQUEST.numerator
    response = client.post("/vending-machine/add-product/", data={"}product_id": "hey"})
    assert int(response.status.split()[0]) == HTTPStatus.BAD_REQUEST.numerator
    response = client.post("/vending-machine/add-product/", data={})
    assert int(response.status.split()[0]) == HTTPStatus.BAD_REQUEST.numerator
    response = client.post("/vending-machine/add-product/", data={"machine_id": 1, "product_id": 1})
    assert int(response.status.split()[0]) == HTTPStatus.BAD_REQUEST.numerator
    response = client.post(
        "/vending-machine/add-product/", data={"machine_id": -400, "product_id": 5000, "quantity": "hey"}
    )
    assert int(response.status.split()[0]) == HTTPStatus.BAD_REQUEST.numerator

    response = client.post("/vending-machine/add-product/", data={"machine_id": 1})
    assert int(response.status.split()[0]) == HTTPStatus.BAD_REQUEST.numerator

    response = client.post("/vending-machine/add-product/", data={"machine_id": 10, "product_id": 4, "quantity": 50})
    assert int(response.status.split()[0]) == HTTPStatus.NOT_FOUND.numerator


def test_edit_product_quantity(app: Flask, client: FlaskClient) -> None:
    response = client.post(
        "/vending-machine/edit-product/", data={"machine_id": "2", "product_id": "3", "quantity": 500}
    )
    print(response.data)
    assert int(response.status.split()[0]) == HTTPStatus.OK.numerator

    response = client.post(
        "/vending-machine/edit-product/", data={"machine_id": "3", "product_id": "3", "quantity": -30}
    )
    print(response.data)
    assert int(response.status.split()[0]) == HTTPStatus.OK.numerator


def test_bad_edit_product_quantity(app: Flask, client: FlaskClient) -> None:
    response = client.post(
        "/vending-machine/edit-product/", data={"machine_id": "1", "product_id": "3", "quantity": 500}
    )
    assert int(response.status.split()[0]) == HTTPStatus.BAD_REQUEST.numerator
    response = client.post(
        "/vending-machine/edit-product/", data={"machine_id": "3", "product_id": "3", "quantity": -399999}
    )
    assert int(response.status.split()[0]) == HTTPStatus.BAD_REQUEST.numerator
    response = client.post(
        "/vending-machine/edit-product/", data={"machine_id": "hey", "product_id": "3", "quantity": -399999}
    )
    assert int(response.status.split()[0]) == HTTPStatus.NOT_FOUND.numerator
    response = client.post(
        "/vending-machine/edit-product/", data={"machine_id": "3", "product_id": "hey", "quantity": -399999}
    )
    assert int(response.status.split()[0]) == HTTPStatus.BAD_REQUEST.numerator

    response = client.post("/vending-machine/edit-product/", data={"product_id": "hey", "quantity": -399999})
    assert int(response.status.split()[0]) == HTTPStatus.BAD_REQUEST.numerator

    response = client.post("/vending-machine/edit-product/", data={"quantity": -399999})
    assert int(response.status.split()[0]) == HTTPStatus.BAD_REQUEST.numerator

    response = client.post("/vending-machine/edit-product/", data={})
    assert int(response.status.split()[0]) == HTTPStatus.BAD_REQUEST.numerator


def test_delete_machine(app: Flask, client: FlaskClient) -> None:
    response = client.post("/vending-machine/delete/", data={"machine_id": "1"})
    assert int(response.status.split()[0]) == HTTPStatus.OK.numerator

    response = client.get("/vending-machine/", query_string={"machine_id": "1"})
    assert int(response.status.split()[0]) == HTTPStatus.NOT_FOUND.numerator


def test_bad_delete_machine(app: Flask, client: FlaskClient) -> None:
    response = client.post("/vending-machine/delete/", data={"machine_id": "1"})
    assert int(response.status.split()[0]) == HTTPStatus.BAD_REQUEST.numerator

    response = client.get("/vending-machine/", query_string={"machine_id": "hello"})
    assert int(response.status.split()[0]) == HTTPStatus.NOT_FOUND.numerator

    response = client.post("/vending-machine/delete/", data={})
    assert int(response.status.split()[0]) == HTTPStatus.BAD_REQUEST.numerator


def test_machine_record(app: Flask, client: FlaskClient) -> None:
    response = client.post("/vending-machine/records", data={"machine_id": 1})
    assert response.status_code == 200
    assert type(response.json) == list


def test_bad_machine_record(app: Flask, client: FlaskClient) -> None:
    response = client.post("/vending-machine/records", data={})
    assert int(response.status.split()[0]) == HTTPStatus.BAD_REQUEST.numerator
