import time


def test_create_list_and_patch_notes(client):
    payload = {"title": "Test", "content": "Hello world"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["title"] == "Test"
    assert "created_at" in data and "updated_at" in data

    r = client.get("/notes/")
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    r = client.get("/notes/", params={"q": "Hello", "limit": 10, "sort": "-created_at"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    note_id = data["id"]
    r = client.patch(f"/notes/{note_id}", json={"title": "Updated"})
    assert r.status_code == 200
    patched = r.json()
    assert patched["title"] == "Updated"


def test_notes_list_limit_skip_and_sort_created_at(client):
    created_ids = []
    for idx in range(5):
        r = client.post(
            "/notes/",
            json={"title": f"Note {idx}", "content": f"Content {idx}"},
        )
        assert r.status_code == 201, r.text
        created_ids.append(r.json()["id"])
        time.sleep(0.001)

    r = client.get("/notes/", params={"sort": "created_at", "limit": 2})
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 2
    assert [item["id"] for item in items] == created_ids[:2]

    r = client.get("/notes/", params={"sort": "created_at", "skip": 2, "limit": 2})
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 2
    assert [item["id"] for item in items] == created_ids[2:4]

    r = client.get("/notes/", params={"sort": "-created_at", "limit": 5})
    assert r.status_code == 200
    items = r.json()
    assert [item["id"] for item in items] == list(reversed(created_ids))


