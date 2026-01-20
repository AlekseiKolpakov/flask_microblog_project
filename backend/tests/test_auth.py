import io


def test_get_tweets_without_api_key(client):
    response = client.get("/api/tweets")

    assert response.status_code == 401

    data = response.get_json()
    assert data["result"] is False
    assert data["error_type"] == "auth_error"


def test_get_tweets_with_invalid_api_key(client):
    response = client.get(
        "/api/tweets",
        headers={"api-key": "invalid"},
    )

    assert response.status_code == 401

    data = response.get_json()
    assert data["result"] is False
    assert data["error_type"] == "auth_error"


def test_create_tweet_unauthorized(client):
    response = client.post(
        "/api/tweets",
        json={"tweet_data": "no auth"},
    )

    assert response.status_code == 401

    data = response.get_json()
    assert data["result"] is False
    assert data["error_type"] == "auth_error"


def test_like_tweet_unauthorized(client, auth_headers):
    # создаём твит
    create = client.post(
        "/api/tweets",
        json={"tweet_data": "like me"},
        headers=auth_headers,
    )
    tweet_id = create.get_json()["tweet_id"]

    # лайк без авторизации
    response = client.post(f"/api/tweets/{tweet_id}/likes")

    assert response.status_code == 401

    json_data = response.get_json()
    assert json_data["result"] is False
    assert json_data["error_type"] == "auth_error"


def test_upload_media_unauthorized(client):
    data = {
        "file": (io.BytesIO(b"fake"), "test.png"),
    }

    response = client.post(
        "/api/medias",
        data=data,
        content_type="multipart/form-data",
    )

    assert response.status_code == 401

    json_data = response.get_json()
    assert json_data["result"] is False
    assert json_data["error_type"] == "auth_error"


def test_delete_foreign_tweet_returns_404(client, auth_headers, second_user):
    # second_user создаёт твит
    headers_user2 = {"api-key": second_user.api_key}

    create = client.post(
        "/api/tweets",
        json={"tweet_data": "foreign"},
        headers=headers_user2,
    )
    tweet_id = create.get_json()["tweet_id"]

    # test-user пытается удалить
    delete = client.delete(
        f"/api/tweets/{tweet_id}",
        headers=auth_headers,
    )

    assert delete.status_code == 404


def test_follow_unauthorized(client, second_user):
    response = client.post(f"/api/users/{second_user.id}/follow")

    assert response.status_code == 401
