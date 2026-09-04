import uuid

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "🚀 Termux API is running"
    assert data["database"] == "SQLite"
    assert data["authentication"] == "JWT"
    assert data["status"] == "online"


def test_register_and_login():
    email = f"test-{uuid.uuid4().hex[:8]}@example.com"
    password = "TestPassword123!"

    # Register
    register = client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "email": email,
            "password": password,
        },
    )

    assert register.status_code == 201

    register_data = register.json()

    assert register_data["name"] == "Test User"
    assert register_data["email"] == email
    assert register_data["message"] == "Registration successful"
    assert "id" in register_data

    # Login
    login = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    assert login.status_code == 200

    login_data = login.json()

    assert "access_token" in login_data
    assert login_data["token_type"] == "bearer"


def test_invalid_authentication():
    email = f"invalid-{uuid.uuid4().hex[:8]}@example.com"

    response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": "WrongPassword123!",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"


def test_user_crud():
    email = f"crud-{uuid.uuid4().hex[:8]}@example.com"

    # Create
    create = client.post(
        "/users",
        json={
            "name": "CRUD User",
            "email": email,
        },
    )

    assert create.status_code == 201

    user = create.json()

    assert user["name"] == "CRUD User"
    assert user["email"] == email
    assert "id" in user

    user_id = user["id"]

    # Read
    get_user = client.get(f"/users/{user_id}")

    assert get_user.status_code == 200
    assert get_user.json()["id"] == user_id

    # Update
    update = client.put(
        f"/users/{user_id}",
        json={
            "name": "Updated User",
            "email": email,
        },
    )

    assert update.status_code == 200
    assert update.json()["name"] == "Updated User"
    assert update.json()["email"] == email

    # Delete
    delete = client.delete(f"/users/{user_id}")

    assert delete.status_code == 200

    # Verify deletion
    deleted = client.get(f"/users/{user_id}")

    assert deleted.status_code == 404
