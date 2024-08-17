import pytest
from app import app as flask_app
from app.data_services import db

@pytest.fixture
def app():
    """
    Fixture to set up and tear down the Flask application for testing.

    Returns:
        Flask: The configured Flask application instance.
    """
    # Configure the Flask app for testing
    flask_app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "postgresql://postgres:ratestask@localhost:5432/postgres",
    })

    # Create the application context and set up the database
    with flask_app.app_context():
        db.create_all()  # Create all database tables
        yield flask_app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()
