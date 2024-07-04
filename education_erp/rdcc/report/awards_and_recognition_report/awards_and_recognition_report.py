# This file contains report code only for filters and columns

import frappe
from frappe import _, msgprint

def execute(filters=None):
    if not filters:
        filters = {}
    if filters.get('award_date'):
        start_date = filters['award_date'][0]
        end_date = filters['award_date'][1]
        filters['award_date'] = ["between", (start_date, end_date)]
    
    data, columns = [], []
    
    columns = get_columns()
    cs_data = get_cs_data(filters)
    
    if not cs_data:
        msgprint(_('No Records Found'))
        return columns, cs_data, None, None, None
    
    data = []
    for d in cs_data:
        row = frappe._dict({
            'instructor': d.instructor,
            'program': d.program,
            'fiscal_year': d.fiscal_year,
            'status': d.status,
            'department': d.department,
            'employee_id': d.employee_id,
            'award': d.award,
            'academic_year': d.academic_year,
            'award_date': d.award_date,
            'institute': d.institute,
            'details': d.details,
            'attachment': d.attachment,
            'approver_hod':d.approver_hod,
            'approver_portfolio_coordinator':d.approver_portfolio_coordinator
        })
        data.append(row)
        
    return columns, data, None, None, None

def get_columns():
    return [
        {
            "fieldname": "program",
            "label": _("Program"),
            "fieldtype": "Link",
            "options": "Program",
            'width': '170'
        },
        {
            "fieldname": "instructor",
            "label": _("Name of Authors"),
            "fieldtype": "Link",
            "options": "Instructor",
            'width': '170'
        },
        {
            "fieldname": "employee_id",
            "label": _("Employee ID"),
            "fieldtype": "Data",
            'width': '170'
        },
        {
            "fieldname": "academic_year",
            "label": _("Academic Year"),
            "fieldtype": "Link",
            "options": "Academic Year",
            'width': '120'
        },
        {
            "fieldname": "award_date",
            "label": _("Award Date"),
            "fieldtype": "Date",
            'width': '120'
        },
        {
            "fieldname": "award",
            "label": _("Award"),
            "fieldtype": "Data",
            'width': '120'
        },
        {
            "fieldname": "department",
            "label": _("Department"),
            "fieldtype": "Link",
            "options":"Department",
            'width': '120'
        },
        {
            "fieldname": "fiscal_year",
            "label": _("Fiscal Year"),
            "fieldtype": "Link",
            "options": "Fiscal Year",
            'width': '120'
        },
        {
            "fieldname": "details",
            "label": _("Details"),
            "fieldtype": "Data",
            'width': '120'
        },
        {
            "fieldname": "status",
            "label": _("Status"),
            "fieldtype": "Data",
            'width': '120'
        },
        {
            "fieldname": "attachment",
            "label": _("Attachment"),
            "fieldtype": "Data",
            'width': '120'
        },
        {
            "fieldname": "approver_portfolio_coordinator",
            "label": _("Approver Portfolio Coordinator"),
            "fieldtype": "Link",
            "options": "Fiscal Year",
            'width': '120'
        },
        {
            "fieldname": "approver_hod",
            "label": _("Approver (HOD)"),
            "fieldtype": "Link",
            "options": "Fiscal Year",
            'width': '120'
        }, 
    ]

def get_cs_data(filters):
    conditions = get_conditions(filters)
    data = frappe.get_all(
        doctype='Awards and Recognition',
        fields=[
            'program', 'instructor', 'employee_id', 'academic_year', 'department', 'fiscal_year', 
            'details', 'status', 'attachment','approver_hod','approver_portfolio_coordinator','award','award_date'
        ],
        filters=conditions
    )
    return data

def get_conditions(filters):
    conditions = {}
    for key, value in filters.items():
        if filters.get(key):
            conditions[key] = value
    return conditions