import json
from typing import List, Optional
from envguardx.utils import load_env_file, is_potentially_unsafe, is_type_match


def check_env_file(env_path: str, schema_path: Optional[str] = None) -> List[str]:
    issues: List[str] = []
    actual_env = load_env_file(env_path)

    if schema_path:
        with open(schema_path, "r") as f:
            schema = json.load(f)

        for key, expected_type in schema.items():
            if key not in actual_env:
                issues.append(f"[schema] Missing variable: {key}")
                continue

            value = actual_env[key]
            if not is_type_match(value, expected_type):
                issues.append(f"[schema] Type mismatch for {key}: expected {expected_type}, got '{value}'")

    for key, value in actual_env.items():
        if is_potentially_unsafe(key, value):
            issues.append(f"Possibly unsafe value: {key}={value}")

    return issues



def generate_env_example(env_path: str, output_path: str) -> None:
    env = load_env_file(env_path)
    with open(output_path, "w") as f:
        for key in env:
            f.write(f"{key}=\n")
