def test_get_tweets(client, auth_headers):
    # Arrange — создаём твит
    client.post(
        "/api/tweets",
        json={"tweet_data": "first tweet"},
        headers=auth_headers,
    )

    # Act
    response = client.get("/api/tweets", headers=auth_headers)

    # Assert
    assert response.status_code == 200

    data = response.get_json()
    assert data["result"] is True
    assert "tweets" in data
    assert isinstance(data["tweets"], list)
    assert len(data["tweets"]) == 1

    tweet = data["tweets"][0]
    assert "id" in tweet
    assert tweet["content"] == "first tweet"
    assert "attachments" in tweet
    assert "author" in tweet
    assert "likes" in tweet
    assert isinstance(tweet["likes"], list)


def test_create_tweet(client, auth_headers):
    # Act
    response = client.post(
        "/api/tweets",
        json={
            "tweet_data": "Hello from pytest",
            "tweet_media_ids": [],
        },
        headers=auth_headers,
    )

    # Assert
    assert response.status_code == 200

    data = response.get_json()
    assert data["result"] is True
    assert "tweet_id" in data
    assert isinstance(data["tweet_id"], int)


def test_delete_own_tweet(client, auth_headers):
    # Arrange — создаём твит
    create = client.post(
        "/api/tweets",
        json={"tweet_data": "delete me"},
        headers=auth_headers,
    )
    tweet_id = create.get_json()["tweet_id"]

    # Act — удаляем свой твит
    delete = client.delete(
        f"/api/tweets/{tweet_id}",
        headers=auth_headers,
    )

    # Assert
    assert delete.status_code == 200
    assert delete.get_json()["result"] is True

    # Проверка: твита больше нет
    response = client.get("/api/tweets", headers=auth_headers)
    tweets = response.get_json()["tweets"]
    assert all(tweet["id"] != tweet_id for tweet in tweets)
