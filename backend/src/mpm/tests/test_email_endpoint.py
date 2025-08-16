import os


def test_email_endpoint(client, monkeypatch):
    # Force MailCatcher mode so we don't send real mail
    monkeypatch.setenv("USE_MAILCATCHER", "true")
    # also override connector to a dummy that always passes?
    # but MailCatcher should accept the SMTP call

    res = client.post(
        "/api/test-email",
        json={"to_address": "test@local", "subject": "Ping", "body": "Hello"},
    )
    assert res.status_code == 200
    assert res.json()["status"] == "sent"
