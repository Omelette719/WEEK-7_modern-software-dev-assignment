import time


def test_create_complete_list_and_patch_action_item(client):
    payload = {"description": "Ship it"}
    r = client.post("/action-items/", json=payload)
    assert r.status_code == 201, r.text
    item = r.json()
    assert item["completed"] is False
    assert "created_at" in item and "updated_at" in item

    r = client.put(f"/action-items/{item['id']}/complete")
    assert r.status_code == 200
    done = r.json()
    assert done["completed"] is True

    r = client.get("/action-items/", params={"completed": True, "limit": 5, "sort": "-created_at"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    r = client.patch(f"/action-items/{item['id']}", json={"description": "Updated"})
    assert r.status_code == 200
    patched = r.json()
    assert patched["description"] == "Updated"


def test_action_items_list_limit_skip_and_sort_created_at(client):
    created_ids = []
    for idx in range(5):
        r = client.post("/action-items/", json={"description": f"Task {idx}"})
        assert r.status_code == 201, r.text
        created_ids.append(r.json()["id"])
        time.sleep(0.001)

    r = client.get("/action-items/", params={"sort": "created_at", "limit": 2})
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 2
    assert [item["id"] for item in items] == created_ids[:2]

    r = client.get(
        "/action-items/", params={"sort": "created_at", "skip": 2, "limit": 2}
    )
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 2
    assert [item["id"] for item in items] == created_ids[2:4]

    r = client.get("/action-items/", params={"sort": "-created_at", "limit": 5})
    assert r.status_code == 200
    items = r.json()
    assert [item["id"] for item in items] == list(reversed(created_ids))


