def test_create_list_get_and_patch_project(client):
    r = client.post("/projects/", json={"name": "Backend Revamp", "description": "Week 7 work"})
    assert r.status_code == 201, r.text
    project = r.json()
    assert project["name"] == "Backend Revamp"
    assert "created_at" in project and "updated_at" in project

    r = client.get("/projects/", params={"q": "Backend", "limit": 10, "sort": "-created_at"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    project_id = project["id"]
    r = client.get(f"/projects/{project_id}")
    assert r.status_code == 200
    fetched = r.json()
    assert fetched["id"] == project_id

    r = client.patch(f"/projects/{project_id}", json={"name": "Backend v2"})
    assert r.status_code == 200
    patched = r.json()
    assert patched["name"] == "Backend v2"


def test_assign_project_to_note_and_action_item(client):
    r = client.post("/projects/", json={"name": "Core"})
    assert r.status_code == 201
    project_id = r.json()["id"]

    r = client.post("/notes/", json={"title": "N1", "content": "C1", "project_id": project_id})
    assert r.status_code == 201, r.text
    note = r.json()
    assert note["project_id"] == project_id

    r = client.post("/action-items/", json={"description": "Do it", "project_id": project_id})
    assert r.status_code == 201, r.text
    item = r.json()
    assert item["project_id"] == project_id


def test_reject_non_existent_project_assignment(client):
    r = client.post("/notes/", json={"title": "N1", "content": "C1", "project_id": 9999})
    assert r.status_code == 404

    r = client.post("/action-items/", json={"description": "Do it", "project_id": 9999})
    assert r.status_code == 404
