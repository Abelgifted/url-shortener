import uuid


def unique_email():
    return f"{uuid.uuid4()}@example.com"


def register_and_login(client):
    email = unique_email()

    client.post("/api/users/register", json={
        "email": email,
        "password": "password123"
    })

    login = client.post("/api/users/login", json={
        "email": email,
        "password": "password123"
    })

    token = login.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


def test_anonymous_url_creation(client):
    response = client.post("/api/urls", json={
        "long_url": "https://example.com"
    })

    assert response.status_code == 201

    data = response.json()

    assert data["click_count"] == 0


def test_authenticated_url_creation(client):
    headers = register_and_login(client)

    response = client.post(
        "/api/urls",
        json={
            "long_url": "https://github.com"
        },
        headers=headers
    )

    assert response.status_code == 201


def test_invalid_url(client):
    response = client.post("/api/urls", json={
        "long_url": "not-a-url"
    })

    assert response.status_code == 422


def test_short_code_length(client):
    response = client.post("/api/urls", json={
        "long_url": "https://example.com"
    })

    code = response.json()["short_code"]

    assert len(code) == 6


def test_redirect(client):
    create = client.post("/api/urls", json={
        "long_url": "https://example.com"
    })

    code = create.json()["short_code"]

    response = client.get(
        f"/{code}",
        follow_redirects=False
    )

    assert response.status_code == 302
    assert response.headers["location"] == "https://example.com/"


def test_stats_returns_correct_data(client):
    create = client.post("/api/urls", json={
        "long_url": "https://example.com"
    })

    code = create.json()["short_code"]

    stats = client.get(f"/api/urls/{code}/stats")

    assert stats.status_code == 200
    assert stats.json()["short_code"] == code


def test_stats_does_not_increment_click_count(client):
    create = client.post("/api/urls", json={
        "long_url": "https://example.com"
    })

    code = create.json()["short_code"]

    first = client.get(f"/api/urls/{code}/stats").json()["click_count"]

    second = client.get(f"/api/urls/{code}/stats").json()["click_count"]

    assert first == second


def test_redirect_increments_click_count(client):
    create = client.post("/api/urls", json={
        "long_url": "https://example.com"
    })

    code = create.json()["short_code"]

    before = client.get(
        f"/api/urls/{code}/stats"
    ).json()["click_count"]

    client.get(
        f"/{code}",
        follow_redirects=False
    )

    after = client.get(
        f"/api/urls/{code}/stats"
    ).json()["click_count"]

    assert after == before + 1


def test_nonexistent_code(client):
    response = client.get("/abcdef")

    assert response.status_code == 404


def test_user_only_sees_own_urls(client):
    headers1 = register_and_login(client)

    headers2 = register_and_login(client)

    client.post(
        "/api/urls",
        json={"long_url": "https://user1.com"},
        headers=headers1
    )

    client.post(
        "/api/urls",
        json={"long_url": "https://user2.com"},
        headers=headers2
    )

    response = client.get(
        "/api/urls",
        headers=headers1
    )

    urls = response.json()

    assert len(urls) == 1
    assert urls[0]["long_url"] == "https://user1.com/"