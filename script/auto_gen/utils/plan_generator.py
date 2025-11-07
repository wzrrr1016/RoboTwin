"""Plan generation utilities."""

import re
from typing import Dict, Any, List
from collections import defaultdict


def match_subplan_to_actions(
    subplan: List[Dict[str, Any]],
    action_descriptions: List[str]
) -> List[Dict[str, Any]]:
    """
    Match each subplan entry to an action description.

    Rules:
    - Match pick/place pairs to action descriptions
    - Skip 'done' actions
    - Only keep first pick and last place for (wrong) actions
    - Only keep first pick and last place for (recovery) actions

    Args:
        subplan: List of subplan entries
        action_descriptions: List of action descriptions from task_info

    Returns:
        List of matched plan entries
    """
    # Group subplan by action pairs (pick + place)
    matched_plan = []
    desc_idx = 0
    i = 0
    while i < len(subplan):
        entry = subplan[i]
        action = entry.get('action', '').lower()
        if action == 'done':
            entry['task_description'] = 'Task completed'
            matched_plan.append(entry)
            i += 1
            continue

        if action == 'pick':
            # Find the corresponding place action
            group = [entry]
            j = i + 1
            while j < len(subplan):
                next_entry = subplan[j]
                next_action = next_entry.get('action', '').lower()
                if next_action == 'place':
                    # Check if it's the same object
                    if (next_entry.get('target_name', []) and
                        entry.get('target_name', []) and
                        next_entry['target_name'][0] == entry['target_name'][0]):
                        group.append(next_entry)
                        break
                j += 1
            
            target_object = subplan[j]['target_name'][0]
            target_container = subplan[j]['target_name'][1] if len(subplan[j]['target_name']) > 1 else ''
            for idx in range(desc_idx, len(action_descriptions)):
                desc = action_descriptions[idx]
                if target_object in desc and target_container in desc:
                    for ij in range(i, j + 1):
                        entry = subplan[ij]
                        entry['task_description'] = desc
                        matched_plan.append(entry)
                    if idx > desc_idx:
                        desc_idx = idx
                    break
            i = j + 1
        else:
            i += 1

    return matched_plan


def filter_plan_by_rules(plan: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Filter plan to keep only:
    - For (wrong): first pick and last place
    - For (recovery): first pick and last place
    - For normal: all actions

    Args:
        plan: List of plan entries

    Returns:
        Filtered list of plan entries
    """
    # Group by task_description
    task_groups = defaultdict(list)
    for entry in plan:
        desc = entry.get('task_description', '')
        task_groups[desc].append(entry)

    filtered = []
    for desc, entries in task_groups.items():
        if '(wrong)' in desc or '(recovery)' in desc:
            # Keep only first pick and last place
            picks = [e for e in entries if e.get('action') == 'pick']
            places = [e for e in entries if e.get('action') == 'place']

            if picks:
                filtered.append(picks[0])  # First pick
            if places:
                filtered.append(places[-1])  # Last place
        else:
            # Keep all actions
            filtered.extend(entries)

    # Sort by frame_idx to maintain order
    filtered.sort(key=lambda x: x.get('frame_idx', 0))
    return filtered


def generate_next_action(plan: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Generate next_action for each plan entry based on rules.

    Rules:
    1. If no (wrong) in task_description, next_action = current action with same target
    2. If (wrong):
       - If action is 'pick', next_action is the first action of the task AFTER recovery task
       - If action is 'place', next_action is 'place' but container changed to 'table'
    3. If (recovery), next_action = current action

    Args:
        plan: List of plan entries

    Returns:
        List of plan entries with next_action added (and without pose field)
    """
    # First pass: identify recovery actions and map wrong description to recovery description
    recovery_desc_map = {}  # Maps wrong description to recovery description

    for i, entry in enumerate(plan):
        desc = entry.get('task_description', '')
        if '(recovery)' in desc:
            # Find the corresponding wrong action
            # Extract object name from recovery description
            obj_match = re.search(r'Pick\s+([^\s]+)', desc)
            if obj_match:
                obj_name = obj_match.group(1)
                # Look backward for the wrong action with the same object
                for j in range(i - 1, -1, -1):
                    prev_desc = plan[j].get('task_description', '')
                    if '(wrong)' in prev_desc and obj_name in prev_desc:
                        recovery_desc_map[prev_desc] = desc
                        break

    # Second pass: generate next_action and remove pose
    result = []
    for i, entry in enumerate(plan):
        desc = entry.get('task_description', '')
        action = entry.get('action', '')
        target_name = entry.get('target_name', [])

        # Create new entry without pose
        new_entry = entry
        if '(wrong)' in desc:
            if action == 'pick':
                # Next action is the first action of the task AFTER recovery
                if desc in recovery_desc_map:
                    recovery_desc = recovery_desc_map[desc]
                    # Find the first task after recovery task
                    found_recovery = False
                    for j in range(i + 1, len(plan)):
                        task_desc = plan[j].get('task_description', '')

                        if task_desc == recovery_desc:
                            found_recovery = True
                            continue

                        # Found the first task after recovery
                        if found_recovery and task_desc != recovery_desc:
                            next_action_val = plan[j].get('action', 'pick')
                            next_target = plan[j].get('target_name', target_name)
                            new_entry['next_action'] = {
                                'action': next_action_val,
                                'target': next_target
                            }
                            break
                    else:
                        # No task after recovery, use current action
                        new_entry['next_action'] = {
                            'action': action,
                            'target': target_name
                        }
                else:
                    # No recovery found, use current action
                    new_entry['next_action'] = {
                        'action': action,
                        'target': target_name
                    }
            elif action == 'place':
                # Target object stays same, but container becomes 'table'
                if len(target_name) >= 2:
                    new_entry['next_action'] = {
                        'action': 'place',
                        'target': [target_name[0], 'table']
                    }
                else:
                    new_entry['next_action'] = {
                        'action': action,
                        'target': target_name
                    }
        else:
            # Normal or recovery action: next_action = current action with same target
            new_entry['next_action'] = {
                'action': action,
                'target': target_name
            }

        result.append(new_entry)

    return result


def generate_plan(
    subplan: List[Dict[str, Any]],
    action_descriptions: List[str]
) -> List[Dict[str, Any]]:
    """
    Generate complete plan from subplan and action descriptions.

    This is the main entry point for plan generation.

    Args:
        subplan: Raw subplan data
        action_descriptions: List of action descriptions from task_info

    Returns:
        Complete plan with task_description and next_action
    """
    # Match subplan to action descriptions
    matched_plan = match_subplan_to_actions(subplan, action_descriptions)

    # Filter by rules (keep first pick and last place for wrong/recovery)
    filtered_plan = filter_plan_by_rules(matched_plan)

    # Generate next_action
    plan_with_next = generate_next_action(filtered_plan)

    return plan_with_next
