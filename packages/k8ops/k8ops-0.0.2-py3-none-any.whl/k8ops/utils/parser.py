#!/usr/bin/env python3

import logging


def parse_cpu(cpu_str: str) -> int:
    """
    Parse CPU resource value and convert it to an integer in millicores

    Examples:
    - "100m" -> 100
    - "0.1" -> 100
    - "1" -> 1000
    """
    if not cpu_str:
        return 0

    if isinstance(cpu_str, int):
        return cpu_str

    cpu_str = str(cpu_str)

    if cpu_str.endswith("m"):
        return int(cpu_str[:-1])
    else:
        # If in decimal form, convert to millicores
        try:
            return int(float(cpu_str) * 1000)
        except ValueError:
            logging.error(f"Unable to parse CPU value: {cpu_str}")
            return 0


def parse_storage(memory_str: str) -> int:
    """
    Parse memory resource value and convert it to an integer in MiB

    Examples:
    - "100Mi" -> 100
    - "1Gi" -> 1024
    - "1G" -> 953  (1000MB)
    - "1000Ki" -> 1
    """
    if not memory_str:
        return 0

    if isinstance(memory_str, int):
        return memory_str

    memory_str = str(memory_str)

    # Define unit conversions
    units = {
        "Ki": 1 / 1024,  # KiB to MiB
        "Mi": 1,  # MiB to MiB
        "Gi": 1024,  # GiB to MiB
        "Ti": 1024 * 1024,  # TiB to MiB
        "K": 1 / 1000,  # KB to MB, then convert to MiB
        "M": 1,  # MB to MiB (approximately)
        "G": 1000,  # GB to MiB (approximately)
        "T": 1000 * 1000,  # TB to MiB (approximately)
    }

    # Try parsing different unit formats
    for unit, multiplier in units.items():
        if memory_str.endswith(unit):
            try:
                value = float(memory_str[: -len(unit)])
                return int(value * multiplier)
            except ValueError:
                continue

    # If no unit, assume bytes
    try:
        return int(int(memory_str) / (1024 * 1024))  # Convert to MiB
    except ValueError:
        logging.error(f"Unable to parse memory value: {memory_str}")
        return 0


def parse_pod_count(pod_count_str: str) -> int:
    """
    Parse pod count resource value and convert it to an integer

    Examples:
    - "100" -> 100
    - "1" -> 1
    - "1k" -> 1000
    """
    if not pod_count_str:
        return 0

    if isinstance(pod_count_str, int):
        return pod_count_str

    pod_count_str = str(pod_count_str)

    if pod_count_str.endswith("k"):
        try:
            return int(float(pod_count_str[:-1]) * 1000)
        except ValueError:
            logging.error(f"Unable to parse Pod count value: {pod_count_str}")
            return 0

    try:
        return int(pod_count_str)
    except ValueError:
        logging.error(f"Unable to parse Pod count value: {pod_count_str}")
        return 0
