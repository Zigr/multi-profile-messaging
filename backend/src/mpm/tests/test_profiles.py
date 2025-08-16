def test_profile_crud(client):
    # Create
    res = client.post(
        "/profiles",
        json={
            "name": "p1",
            "platform": "email",
            "credentials": {"user": "a", "password": "b"},
            "proxy": None,
        },
    )
    assert res.status_code == 201
    data = res.json()
    pid = data["id"]
    assert data["name"] == "p1"

    # Read
    res = client.get(f"/profiles/{pid}")
    assert res.status_code == 200
    assert res.json()["platform"] == "email"

    # Update
    res = client.put(
        f"/profiles/{pid}",
        json={
            "name": "p1-new",
            "platform": "email",
            "credentials": {"user": "a", "password": "b"},
            "proxy": "http://127.0.0.1:8080",
        },
    )
    assert res.status_code == 200
    assert res.json()["name"] == "p1-new"
    assert res.json()["proxy"].startswith("http")

    # Delete
    res = client.delete(f"/profiles/{pid}")
    assert res.status_code == 204

    # Confirm deletion
    res = client.get(f"/profiles/{pid}")
    assert res.status_code == 404
