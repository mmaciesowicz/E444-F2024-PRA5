import pytest
from application import app, load_model

# Load the model and vectorizer as they are needed for mock tests
loaded_model, vectorizer = load_model()

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_real_news(client):
    # Example of real news input
    real_news_1 = "This is real news"

    response = client.post('/', data={'sentence': real_news_1})
    assert response.status_code == 200
    assert b"Prediction" in response.data
    assert b"REAL" in response.data

    real_news_2 = "Summer is hot."

    response = client.post('/', data={'sentence': real_news_2})
    assert response.status_code == 200
    assert b"Prediction" in response.data
    assert b"REAL" in response.data


def test_fake_news(client):
    # Example of fake news input
    fake_news_1 = "This is fake news"

    response = client.post('/', data={'sentence': fake_news_1})
    assert response.status_code == 200
    assert b"Prediction" in response.data
    assert b"FAKE" in response.data

    fake_news_2 = "Summer is cold"

    response = client.post('/', data={'sentence': fake_news_2})
    assert response.status_code == 200
    assert b"Prediction" in response.data
    assert b"FAKE" in response.data

