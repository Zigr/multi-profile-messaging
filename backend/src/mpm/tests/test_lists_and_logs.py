def test_list_and_log_crud(client):
    # First, create a profile to attach list entries/logs to
    res = client.post("/profiles", json={
        "name": "p2",
        "platform": "email",
        "credentials": {"user":"x","password":"y"},
        "proxy": None
    })
    pid = res.json()["id"]

    # Create a whitelist entry
    res = client.post("/lists", json={
        "profile_id": pid,
        "type": "whitelist",
        "value": "foo@example.com"
    })
    assert res.status_code == 201
    entry_id = res.json()["id"]

    # Filter lists
    res = client.get(f"/lists?profile_id={pid}&type=whitelist")
    assert any(e["id"] == entry_id for e in res.json())

    # Create a fake log entry directly in DB (or via endpoint if you have one)
    # For now, assume logs get written by your worker; test that GET /logs works:
    res = client.get(f"/logs?profile_id={pid}")
    assert res.status_code == 200
    assert isinstance(res.json(), list)

    # Cleanup
    client.delete(f"/lists/{entry_id}")
    client.delete(f"/profiles/{pid}")
