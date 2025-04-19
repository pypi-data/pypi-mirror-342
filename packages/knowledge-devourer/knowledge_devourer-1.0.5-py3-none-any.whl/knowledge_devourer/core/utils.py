import datetime
from typing import Any, Tuple


def load_links(path: str, limit: int = None) -> list[str]:
    with open(path, "r") as fh:
        if not limit:
            return [line.strip() for line in fh if line.strip() and not line.startswith("#")]
        else:
            return [line.strip() for line in fh if line.strip() and not line.startswith("#")][:limit:]


def to_dict_recursively(obj: Any) -> Any:
    """
    Convert objects to JSON‐serializable structures,
    turning datetime/date/time into ISO strings.
    """
    if isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
        return obj.isoformat()

    if isinstance(obj, dict):
        return {k: to_dict_recursively(v) for k, v in obj.items()}

    if isinstance(obj, (list, tuple)):
        return type(obj)(to_dict_recursively(v) for v in obj)

    if hasattr(obj, "__dict__"):
        return {k: to_dict_recursively(v) for k, v in vars(obj).items()}

    return obj


def extract_content_type_and_content_id_from_link(link: str) -> Tuple[str, str]:
    """
    Parse Instagram URLs to get content type and ID.
    """
    if "reel/" in link:
        return "reel", link.split("reel/")[1].split("/")[0]
    if "p/" in link:
        return "post", link.split("p/")[1].split("/")[0]
    raise ValueError(f"Can't parse content type and content id from: {link}")
