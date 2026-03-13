import re


TODO_PATTERN = re.compile(r"^\s*(?:[-*]\s*)?TODO\b\s*[:\-]?\s*(.+)$", re.IGNORECASE)
ACTION_PATTERN = re.compile(r"^\s*(?:[-*]\s*)?ACTION\b\s*[:\-]?\s*(.+)$", re.IGNORECASE)
BULLET_PATTERN = re.compile(r"^\s*[-*]\s+(.+)$")


def _clean_description(description: str) -> str:
    return description.strip()


def extract_action_items(text: str) -> list[str]:
    results: list[str] = []

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if not line.strip():
            continue

        match = TODO_PATTERN.match(line) or ACTION_PATTERN.match(line) or BULLET_PATTERN.match(line)
        if not match:
            continue

        description = _clean_description(match.group(1))
        if description:
            results.append(description)

    return results


