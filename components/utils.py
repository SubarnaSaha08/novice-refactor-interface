def is_task_complete(response_data, session_id):
    if session_id == 1:
        required_keys = [
            "difficulty",
            "code_understanding",
            "logic_flow",
            "function_identification",
            "code_structure",
            "open_ended_1",
            "open_ended_2",
            "mental_demand",
            "physical_demand",
            "temporal_demand",
            "performance",
            "effort",
            "frustration",
        ]
    elif session_id == 2:
        required_keys = [
            "code_understanding",
            "logic_flow",
            "function_identification",
            "code_structure",
            "open_ended_1",
            "open_ended_2",
            "mental_demand",
            "physical_demand",
            "temporal_demand",
            "performance",
            "effort",
            "frustration",
            "overall_effectiveness",
            "support_for_learning",
            "confidence_boost",
            "impact_on_approach",
        ]

    for key in required_keys:
        val = response_data.get(key)
        # For radio buttons, None means incomplete
        # For text inputs, empty string or None means incomplete
        if val is None or (isinstance(val, str) and val.strip() == ""):
            return False
    return True
