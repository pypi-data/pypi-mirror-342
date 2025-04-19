from typing import Dict


def load_env_file(path: str) -> Dict[str, str]:
    env: Dict[str, str] = {}
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            env[key.strip()] = value.strip()
    return env


def is_potentially_unsafe(key: str, value: str) -> bool:
    key_lower = key.lower()
    value_lower = value.lower()

    if "debug" in key_lower and value_lower in ("true", "1"):
        return True
    if "secret" in key_lower and (not value or value == "12345"):
        return True
    if "token" in key_lower and len(value) < 10:
        return True
    return False

def is_type_match(value: str, expected: str) -> bool:
    try:
        if expected == "int":
            int(value)
        elif expected == "float":
            float(value)
        elif expected == "bool":
            return value.lower() in {"true", "false", "1", "0"}
        elif expected == "string":
            return True
        else:
            return False
        return True
    except ValueError:
        return False
