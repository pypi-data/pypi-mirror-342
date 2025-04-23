import yaml
import os
from typing import Dict, Any


def deep_merge(source: Dict[str, Any], destination: Dict[str, Any]) -> Dict[str, Any]:
    """
    Deep merge two dictionaries
    """
    for key, value in source.items():
        if (
            isinstance(value, dict)
            and key in destination
            and isinstance(destination[key], dict)
        ):
            # If both values are dictionaries, recursively merge them
            destination[key] = deep_merge(value, destination[key])
        else:
            # Otherwise, source value overrides destination
            destination[key] = value
    return destination


def load_helm_values(
    chart_name: str,
    cluster_name: str,
    common_values_path: str,
    cluster_values_path: str,
    *additional_files: str,
) -> Dict[str, Any]:
    """
    Load and merge Helm values files, later files are more important
    """
    paths = [
        os.path.join("charts", chart_name, "values.yaml"),
        os.path.join(common_values_path, "common.yaml"),
        os.path.join(common_values_path, f"{chart_name}.yaml"),
        os.path.join(cluster_values_path, cluster_name, "common.yaml"),
        os.path.join(cluster_values_path, cluster_name, f"{chart_name}.yaml"),
        *additional_files,
    ]

    result: Dict[str, Any] = {}

    for path in paths:
        if os.path.exists(path):
            with open(path, "r") as f:
                values = yaml.safe_load(f) or {}
                result = deep_merge(values, result)

    return result
