# All variable names for task information must be in uppercase.

TASK_INFO_CONSTRAINT = {
    "task_name": "medicine_into_safe_tray",
    "task_description":
    "scene: A medicine_bottle, a safe_tray, and a forbidden_zone are present./"
    "task: Respect the constraint: do not cross the forbidden_zone; place the medicine_bottle only into the safe_tray./"
    "action: Move medicine_bottle into safe_tray while avoiding forbidden_zone at all times."
}

task_info_constraint = TASK_INFO_CONSTRAINT

