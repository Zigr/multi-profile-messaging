def test_template_crud(client):
    # Create
    res = client.post(
        "/templates",
        json={
            "name": "welcome",
            "subject": "Hi {Name}",
            "body": "Hello {Name}, welcome!",
        },
    )
    assert res.status_code == 201
    tid = res.json()["id"]

    # List & fetch
    res = client.get("/templates")
    assert res.status_code == 200
    assert any(t["id"] == tid for t in res.json())

    res = client.get(f"/templates/{tid}")
    assert res.status_code == 200
    assert "welcome" in res.json()["name"]

    # Update
    res = client.put(
        f"/templates/{tid}",
        json={"name": "welcome2", "subject": "Hello {Name}", "body": "Hey {Name}!"},
    )
    assert res.json()["name"] == "welcome2"

    # Delete
    res = client.delete(f"/templates/{tid}")
    assert res.status_code == 204
