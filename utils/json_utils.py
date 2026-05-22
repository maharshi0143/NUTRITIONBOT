import json
import re
from typing import Any, Dict


def extract_json(text: str) -> Dict[str, Any]:
    """Extract the first JSON object from text."""
    if not text:
        return {}

    match = re.search(r"\{[\s\S]*\}", text)
    if not match:
        return {}

    try:
        return json.loads(match.group(0))
    except json.JSONDecodeError:
        return {}
