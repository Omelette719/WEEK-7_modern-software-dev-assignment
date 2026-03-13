from backend.app.services.extract import extract_action_items


def test_extract_action_items():
    text = """
    This is a note
    - TODO: write tests
    - ACTION: review PR
    TODO fix login flow
    Action - sync with design
    * Prepare demo slides
    - Ship it!
    Not actionable
    """.strip()

    items = extract_action_items(text)
    assert items == [
        "write tests",
        "review PR",
        "fix login flow",
        "sync with design",
        "Prepare demo slides",
        "Ship it!",
    ]


