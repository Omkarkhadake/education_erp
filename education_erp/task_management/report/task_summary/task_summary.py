

# Copyright (c) 2024, ppcrc and contributors
# For license information, please see license.txt

import frappe
import json
from frappe import _
from frappe.utils import date_diff, nowdate

def execute(filters=None):
    columns, data = [], []
    data = get_data(filters)
    columns = get_columns(data)
    charts = get_chart_data(data)
    return columns, data, None, charts

# def get_data(filters):
#     conditions = get_conditions(filters)
#     tasks = frappe.get_all(
#         "Task Entry",
#         filters=conditions,
#         fields=[
#             "task_name",
#             "owner",
#             "entity_name",
#             "regulating_authority",
#             "expected_start_date",
#             "expected_end_date",
#             "task_category",
#             "task_sub_category",
#             "task_frequency",
#             "status",
#             "priority",
#             "task_due_date",
#             "completed_on",
#             "_assign",
            
#         ],
#         order_by="creation",
#     )
    
#     # Determine the maximum number of assignees
#     max_assigns = 0
#     for task in tasks:
#         task._assign = json.loads(task._assign) if task._assign else []
#         max_assigns = max(max_assigns, len(task._assign))
    
#     # Add assignee data as separate fields
#     for task in tasks:
#         if task.task_due_date:
#             if task.completed_on:
#                 task.delay = date_diff(task.completed_on, task.task_due_date)
#             elif task.status == "Completed":
#                 # task is completed but completed_on is not set (for older tasks)
#                 task.delay = 0
#             else:
#                 # task not completed
#                 task.delay = date_diff(nowdate(), task.task_due_date)
#         else:
#             # task has no end date, hence no delay
#             task.delay = 0

#         task.status = _(task.status)
#         task.priority = _(task.priority)
        
#         # Add assignees to the task data
#         for i in range(max_assigns):
#             task[f"assigned_to_{i+1}"] = task._assign[i] if i < len(task._assign) else ""

#     # Sort by descending order of delay
#     tasks.sort(key=lambda x: x["delay"], reverse=True)
#     return tasks


def get_data(filters):
    conditions = get_conditions(filters)
    tasks = frappe.get_all(
        "Task Entry",
        filters=conditions,
        fields=[
            "task_name",
            "owner",
            "entity_name",
            "regulating_authority",
            "expected_start_date",
            "expected_end_date",
            "task_category",
            "task_sub_category",
            "task_frequency",
            "status",
            "priority",
            "task_due_date",
            "completed_on",
            "_assign",
        ],
        order_by="creation",
    )
    
    if not tasks:
        return []

    # Determine the maximum number of assignees
    max_assigns = 0
    for task in tasks:
        task._assign = json.loads(task._assign) if task._assign else []
        max_assigns = max(max_assigns, len(task._assign))

    # Add assignee data as separate fields
    for task in tasks:
        if task.task_due_date:
            if task.completed_on:
                task.delay = date_diff(task.completed_on, task.task_due_date)
            elif task.status == "Completed":
                task.delay = 0
            else:
                task.delay = date_diff(nowdate(), task.task_due_date)
        else:
            task.delay = 0

        task.status = _(task.status)
        task.priority = _(task.priority)

        for i in range(max_assigns):
            task[f"assigned_to_{i+1}"] = task._assign[i] if i < len(task._assign) else ""

    tasks.sort(key=lambda x: x["delay"], reverse=True)
    return tasks


def get_conditions(filters):
    conditions = frappe._dict()
    keys = ["priority", "status"]
    for key in keys:
        if filters.get(key):
            conditions[key] = filters.get(key)
    if filters.get("from_date"):
        conditions.expected_end_date = [">=", filters.get("from_date")]
    if filters.get("to_date"):
        conditions.expected_start_date = ["<=", filters.get("to_date")]
    return conditions

def get_chart_data(data):
    delay, on_track, overdue = 0, 0, 0
    for entry in data:
        if entry.get("completed_on") and entry.get("completed_on") > entry.get("expected_end_date"):
            overdue += 1
        elif entry.get("delay") > 0:
            delay += 1
        else:
            on_track += 1
    
    charts = {
        "data": {
            "labels": [_("On Track"), _("Delayed"), _("Overdue")],
            "datasets": [{"name": "Task Status", "values": [on_track, delay, overdue]}],
        },
        "type": "percentage",
        "colors": ["#84D5BA", "#CB4B5F", "#FFA500"],  # Added a new color for "Overdue"
    }
    return charts

# def get_columns(data):
#     # Basic columns
#     columns = [
#         {"fieldname": "task_name", "fieldtype": "Link", "label": _("Task Name"), "options": "Task", "width": 150},
#         {"fieldname": "owner", "fieldtype": "Data", "label": _("Created By"), "width": 120},
#         {"fieldname": "entity_name", "fieldtype": "Link", "label": _("Entity Name"), "options": "Company", "width": 200},
#         {"fieldname": "status", "fieldtype": "Data", "label": _("Status"), "width": 100},
#         {"fieldname": "priority", "fieldtype": "Data", "label": _("Priority"), "width": 80},
#         {"fieldname": "task_frequency", "fieldtype": "Data", "label": _("Task Frequency"), "width": 80},
#         {"fieldname": "regulating_authority", "fieldtype": "Link", "label": _("Regulating Authority"), "options": "Regulating Authority", "width": 120},
#         {"fieldname": "task_category", "fieldtype": "Link", "label": _("Task Category"), "options": "Task Category", "width": 120},
#         {"fieldname": "task_sub_category", "fieldtype": "Link", "label": _("Task Sub-Category"), "options": "Task Sub-Category", "width": 120},
#         {"fieldname": "expected_start_date", "fieldtype": "Date", "label": _("Expected Start Date"), "width": 150},
#         {"fieldname": "expected_end_date", "fieldtype": "Date", "label": _("Expected End Date"), "width": 150},
#         {"fieldname": "task_due_date", "fieldtype": "Date", "label": _("Task Due Date"), "width": 150},
#         {"fieldname": "completed_on", "fieldtype": "Date", "label": _("Completed On"), "width": 150},                        
#         {"fieldname": "delay", "fieldtype": "Data", "label": _("Delay (In Days)"), "width": 120},
#     ]

#     # Dynamically add columns for each assigned user
#     max_assigns = max(len(task['_assign']) for task in data)
#     for i in range(max_assigns):
#         columns.append({"fieldname": f"assigned_to_{i+1}", "fieldtype": "Data", "label": _(f"Assigned To {i+1}"), "width": 150})

#     return columns

def get_columns(data):
    # Basic columns
    columns = [
        {"fieldname": "task_name", "fieldtype": "Link", "label": _("Task Name"), "options": "Task", "width": 150},
        {"fieldname": "owner", "fieldtype": "Data", "label": _("Created By"), "width": 120},
        {"fieldname": "entity_name", "fieldtype": "Link", "label": _("Entity Name"), "options": "Company", "width": 200},
        {"fieldname": "status", "fieldtype": "Data", "label": _("Status"), "width": 100},
        {"fieldname": "priority", "fieldtype": "Data", "label": _("Priority"), "width": 80},
        {"fieldname": "task_frequency", "fieldtype": "Data", "label": _("Task Frequency"), "width": 80},
        {"fieldname": "regulating_authority", "fieldtype": "Link", "label": _("Regulating Authority"), "options": "Regulating Authority", "width": 120},
        {"fieldname": "task_category", "fieldtype": "Link", "label": _("Task Category"), "options": "Task Category", "width": 120},
        {"fieldname": "task_sub_category", "fieldtype": "Link", "label": _("Task Sub-Category"), "options": "Task Sub-Category", "width": 120},
        {"fieldname": "expected_start_date", "fieldtype": "Date", "label": _("Expected Start Date"), "width": 150},
        {"fieldname": "expected_end_date", "fieldtype": "Date", "label": _("Expected End Date"), "width": 150},
        {"fieldname": "task_due_date", "fieldtype": "Date", "label": _("Task Due Date"), "width": 150},
        {"fieldname": "completed_on", "fieldtype": "Date", "label": _("Completed On"), "width": 150},
        {"fieldname": "delay", "fieldtype": "Data", "label": _("Delay (In Days)"), "width": 120},
    ]

    # Check if data is empty
    if not data:
        return columns

    # Dynamically add columns for each assigned user
    max_assigns = max(len(task['_assign']) for task in data)
    for i in range(max_assigns):
        columns.append({"fieldname": f"assigned_to_{i+1}", "fieldtype": "Data", "label": _(f"Assigned To {i+1}"), "width": 150})

    return columns
