import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    yield client

def test_homepage(client):
    response = client.get("/")

    assert response.status_code == 200

    expected_content = b"<h1> Welcome Home </h1>"
    assert expected_content in response.data, f"Expected '{expected_content}' in response"

