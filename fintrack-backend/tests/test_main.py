import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.database import get_session
from app.main import app
from app.models import TransactionType


@pytest.fixture(name="client")
def client_fixture(session: Session):
    app.dependency_overrides[get_session] = lambda: session
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture
def auth_headers(client: TestClient, default_user):
    # Create the user first
    client.post("/users", json=default_user.model_dump())
    
    # Login
    response = client.post(
        "/auth/login",
        data={"username": default_user.email, "password": default_user.password},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_user_flow(client: TestClient):
    # 1. Create a user
    response = client.post(
        "/users",
        json={"name": "Alice", "email": "alice@example.com", "password": "password123"},
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Alice"
    assert response.json()["email"] == "alice@example.com"

    # 2. Login
    login_response = client.post(
        "/auth/login",
        data={"username": "alice@example.com", "password": "password123"},
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 3. List users (should see Alice)
    list_response = client.get("/users")
    assert list_response.status_code == 200
    assert len(list_response.json()) >= 1

    # 4. Update user
    update_response = client.patch(
        "/users", json={"name": "Alice Updated"}, headers=headers
    )
    assert update_response.status_code == 200
    assert update_response.json()["name"] == "Alice Updated"

    # 5. Delete user
    delete_response = client.delete("/users", headers=headers)
    assert delete_response.status_code == 204


def test_login_invalid_credentials(client: TestClient):
    response = client.post(
        "/auth/login",
        data={"username": "notfound@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 404


def test_account_flow(client: TestClient, auth_headers):
    # 1. Create account
    create_response = client.post(
        "/accounts", json={"name": "Savings", "balance": 1000}, headers=auth_headers
    )
    assert create_response.status_code == 201
    account_id = create_response.json()["id"]
    assert create_response.json()["name"] == "Savings"
    assert create_response.json()["balance"] == 1000

    # 2. List accounts
    list_response = client.get("/accounts", headers=auth_headers)
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1
    assert list_response.json()[0]["id"] == account_id

    # 3. Update account
    update_response = client.patch(
        f"/accounts/{account_id}", json={"name": "Main Savings"}, headers=auth_headers
    )
    assert update_response.status_code == 200
    assert update_response.json()["name"] == "Main Savings"

    # 4. Cannot delete account with balance
    delete_response_bad = client.delete(f"/accounts/{account_id}", headers=auth_headers)
    assert delete_response_bad.status_code == 409

    # Note: We can't easily delete account with balance 1000, 
    # we would need to spend it first or manually alter DB. We'll leave it as is.


def test_transaction_flow(client: TestClient, auth_headers):
    # 1. Create two accounts
    acc1_res = client.post("/accounts", json={"name": "Wallet", "balance": 500}, headers=auth_headers)
    acc1_id = acc1_res.json()["id"]

    acc2_res = client.post("/accounts", json={"name": "Bank", "balance": 0}, headers=auth_headers)
    acc2_id = acc2_res.json()["id"]

    # 2. Create INCOME transaction
    income_res = client.post(
        "/transactions",
        json={"source_account": acc1_id, "amount": 200, "type": "income", "description": "Salary"},
        headers=auth_headers
    )
    assert income_res.status_code == 201
    
    # Wallet should now have 700
    accounts = client.get("/accounts", headers=auth_headers).json()
    wallet = next(a for a in accounts if a["id"] == acc1_id)
    assert wallet["balance"] == 700

    # 3. Create EXPENSE transaction
    expense_res = client.post(
        "/transactions",
        json={"source_account": acc1_id, "amount": 100, "type": "expense", "description": "Food"},
        headers=auth_headers
    )
    assert expense_res.status_code == 201
    
    # Wallet should now have 600
    accounts = client.get("/accounts", headers=auth_headers).json()
    wallet = next(a for a in accounts if a["id"] == acc1_id)
    assert wallet["balance"] == 600

    # 4. Create TRANSFER transaction
    transfer_res = client.post(
        "/transactions",
        json={"source_account": acc1_id, "destination_account": acc2_id, "amount": 600, "type": "transfer", "description": "Move all out"},
        headers=auth_headers
    )
    assert transfer_res.status_code == 201
    transfer_id = transfer_res.json()["id"]

    # Wallet should have 0, Bank should have 600
    accounts = client.get("/accounts", headers=auth_headers).json()
    wallet = next(a for a in accounts if a["id"] == acc1_id)
    bank = next(a for a in accounts if a["id"] == acc2_id)
    assert wallet["balance"] == 0
    assert bank["balance"] == 600

    # 5. Reverse TRANSFER (Delete)
    del_res = client.delete(f"/transactions/{transfer_id}", headers=auth_headers)
    assert del_res.status_code == 204

    # Wallet should be back to 600, Bank to 0
    accounts = client.get("/accounts", headers=auth_headers).json()
    wallet = next(a for a in accounts if a["id"] == acc1_id)
    bank = next(a for a in accounts if a["id"] == acc2_id)
    assert wallet["balance"] == 600
    assert bank["balance"] == 0
