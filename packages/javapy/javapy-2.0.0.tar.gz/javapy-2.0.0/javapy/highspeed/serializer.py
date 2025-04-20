import struct
from typing import Dict, Any

def _flatten_dict(d: Dict, parent_key: str = "", sep: str = ".") -> Dict:
    """Ubah nested dict menjadi flat dict."""
    items = {}
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.update(_flatten_dict(v, new_key, sep))
        else:
            items[new_key] = v
    return items

def pack_data(data: Dict) -> bytes:
    """Serialize nested dict ke binary."""
    flat = _flatten_dict(data)
    packed = bytearray()
    for key, value in flat.items():
        key_bytes = key.encode("utf-8")
        value_bytes = str(value).encode("utf-8")
        packed.extend(struct.pack("!I", len(key_bytes)))
        packed.extend(key_bytes)
        packed.extend(struct.pack("!I", len(value_bytes)))
        packed.extend(value_bytes)
    return bytes(packed)
