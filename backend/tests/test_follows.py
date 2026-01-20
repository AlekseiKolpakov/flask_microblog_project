def test_follow_user(client, auth_headers, second_user):
    follow = client.post(
        f"/api/users/{second_user.id}/follow",
        headers=auth_headers,
    )

    assert follow.status_code == 200
    assert follow.get_json()["result"] is True


def test_unfollow_user(client, auth_headers, second_user):
    unfollow = client.delete(
        f"/api/users/{second_user.id}/follow",
        headers=auth_headers,
    )

    assert unfollow.status_code == 200
    assert unfollow.get_json()["result"] is True
