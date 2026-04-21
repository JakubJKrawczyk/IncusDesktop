from typing import Dict


class StatusCode:
    CODES = {
        100: "OPERATION_CREATED",
        101: "STARTED",
        102: "STOPPED",
        103: "RUNNING",
        104: "CANCELING",
        105: "PENDING",
        106: "STARTING",
        107: "STOPPING",
        108: "ABORTING",
        109: "FREEZING",
        110: "FROZEN",
        111: "THAWED",
        112: "ERROR",
        113: "READY",
        200: "SUCCESS",
        400: "FAILURE",
        401: "CANCELED",
        500: "INTERNAL_SERVER_ERROR"

    }