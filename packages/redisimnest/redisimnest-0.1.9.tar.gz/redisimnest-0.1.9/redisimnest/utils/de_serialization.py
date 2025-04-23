import json
from datetime import datetime
from uuid import UUID
from typing import Any, Union


def serialize(value: Any) -> bytes:
    """Serializes a value into bytes with embedded type metadata."""
    if isinstance(value, datetime):
        data = {"__type__": "datetime", "value": value.isoformat()}
    elif isinstance(value, UUID):
        data = {"__type__": "uuid", "value": str(value)}
    elif isinstance(value, tuple):
        data = {"__type__": "tuple", "value": list(value)}
    elif isinstance(value, bool):
        data = {"__type__": "bool", "value": value}
    elif isinstance(value, (int, float, str)):
        data = {"__type__": type(value).__name__, "value": value}
    elif isinstance(value, (dict, list)):
        data = {"__type__": type(value).__name__, "value": value}
    else:
        raise TypeError(f"Unsupported value type: {type(value)}")
    
    return json.dumps(data).encode()


def deserialize(raw: Union[bytes, str]) -> Any:
    """Deserializes bytes or string into Python object based on embedded __type__."""
    if isinstance(raw, bytes):
        raw = raw.decode()

    data = json.loads(raw)

    if not isinstance(data, dict) or "__type__" not in data:
        raise ValueError("Missing __type__ metadata in serialized data")

    value_type = data["__type__"]
    value = data["value"]

    if value_type == "datetime":
        return datetime.fromisoformat(value)
    elif value_type == "uuid":
        return UUID(value)
    elif value_type == "tuple":
        return tuple(value)
    elif value_type == "bool":
        return bool(value)
    elif value_type == "int":
        return int(value)
    elif value_type == "float":
        return float(value)
    elif value_type == "str":
        return str(value)
    elif value_type == "list":
        return list(value)
    elif value_type == "dict":
        return dict(value)
    else:
        raise TypeError(f"Unsupported deserialization type: {value_type}")
