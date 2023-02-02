import typing

import pytest
from flask import Flask
from flask.testing import FlaskClient, FlaskCliRunner
from app import create_app
from config import Config


@pytest.fixture(scope="session")
def app() -> typing.Generator:
    app = create_app(config_class=Config())
    app.config.update(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": Config.SQLALCHEMY_DATABASE_URI,
        }
    )
    yield app


@pytest.fixture(scope="session")
def client(app: Flask) -> FlaskClient:
    return app.test_client()


@pytest.fixture(scope="session")
def runner(app: Flask) -> FlaskCliRunner:
    return app.test_cli_runner()
