from typing import Literal, cast

BuildingStatus = Literal[
    "COMPLETED",
    "DRAFT",
    "FAILED_BASELINE",
    "FAILED_STRATEGIES",
    "NOT_STARTED",
    "QUEUED_BASELINE",
    "QUEUED_STRATEGIES",
    "RUNNING_BASELINE",
    "RUNNING_STRATEGIES",
]

BUILDING_STATUS_VALUES: set[BuildingStatus] = {
    "COMPLETED",
    "DRAFT",
    "FAILED_BASELINE",
    "FAILED_STRATEGIES",
    "NOT_STARTED",
    "QUEUED_BASELINE",
    "QUEUED_STRATEGIES",
    "RUNNING_BASELINE",
    "RUNNING_STRATEGIES",
}


def check_building_status(value: str) -> BuildingStatus:
    if value in BUILDING_STATUS_VALUES:
        return cast(BuildingStatus, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {BUILDING_STATUS_VALUES!r}")
