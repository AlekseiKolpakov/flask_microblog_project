import io


def test_upload_media(client, auth_headers):
    data = {
        "file": (io.BytesIO(b"fake image data"), "test.png"),
    }

    response = client.post(
        "/api/medias",
        data=data,
        headers=auth_headers,
        content_type="multipart/form-data",
    )

    assert response.status_code == 200

    json_data = response.get_json()
    assert json_data["result"] is True
    assert "media_id" in json_data
