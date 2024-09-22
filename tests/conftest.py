import pytest
from app import create_app, db

@pytest.fixture(scope='module')
def test_client():
    app = create_app('testing')  # Use the appropriate config for testing
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Create tables
            yield client
            db.drop_all()  # Clean up after tests
