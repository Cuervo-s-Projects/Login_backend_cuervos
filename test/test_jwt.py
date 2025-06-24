from flask_jwt_extended import create_access_token

def test_valid_token(client, app):
    with app.app_context():
        token = create_access_token(identity="user123")

    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/profile", headers=headers)

    assert response.status_code == 200

def test_invalid_token(client):
    headers = {"Authorization": "Bearer invalid.token.here"}
    response = client.get("/api/profile", headers=headers)
    assert response.status_code == 422 
