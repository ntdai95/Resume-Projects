from fastapi.testclient import TestClient
from app.main import app


def test_predict_endpoint():
    client = TestClient(app)
    response = client.post("/predict", json={"hour": 12, "dayofyear": 150, "lag_1": 13.2,
                                             "lag_3": 13.1, "lag_6": 13.0})

    assert response.status_code in [200, 404]