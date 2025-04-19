from typing import List

def get_device_count() -> int:
    """
    Get the number of MLU devices available on the system.

    Returns:
        int: The number of MLU devices.
    """
    ...

def get_core_utilizations(card_id: int) -> List[int]:
    """
    Get the core utilization of a specific MLU device.
    """
    ...