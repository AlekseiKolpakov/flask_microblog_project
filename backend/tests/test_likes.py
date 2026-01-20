def test_like_and_unlike_tweet(client, auth_headers, second_user):
    # user1 создаёт твит
    create = client.post(
        "/api/tweets",
        json={"tweet_data": "like me"},
        headers=auth_headers,
    )
    tweet_id = create.get_json()["tweet_id"]

    # user2 лайкает
    headers_user2 = {"api-key": second_user.api_key}

    like = client.post(
        f"/api/tweets/{tweet_id}/likes",
        headers=headers_user2,
    )

    assert like.status_code == 200
    assert like.get_json()["result"] is True

    # user2 анлайкает
    unlike = client.delete(
        f"/api/tweets/{tweet_id}/likes",
        headers=headers_user2,
    )

    assert unlike.status_code == 200
    assert unlike.get_json()["result"] is True
