import frappe
from frappe import _, msgprint

def execute(filters=None):
    associated_programs = get_associated_programs()
    if not filters:
        filters = {}

    if filters.get('filed_date'):
        start_date = filters['filed_date'][0]
        end_date = filters['filed_date'][1]
        filters['filed_date'] = ["between", (start_date, end_date)]

    data, columns = [], []
    columns = get_columns()  # Populate the columns list
    cs_data = get_cs_data(filters, associated_programs)

    if not cs_data:
        msgprint(_('No Records Found'))
        return columns, cs_data, None, None, None

    data = []
    for d in cs_data:
        row = frappe._dict({
            'ipr': d.ipr,
            'academic_year': d.academic_year,
            'filed_date': d.filed_date,
            'instructors': d.instructors,
            'employee_id': d.employee_id,
            'program': d.program,
            'affiliation': d.affiliation,
            'finacial_year': d.finacial_year,  # Corrected typo here
            'title': d.title,
            'application_no': d.application_no,
            'published_date_or_granted_date': d.published_date_or_granted_date,
            'status': d.status,
            'publication_number_or_granted_number': d.publication_number_or_granted_number,
            'registration_no': d.registration_no,
            'status_of_ipr': d.status_of_ipr,
            'attachment': d.attachment
        })
        data.append(row)

    chart = get_chart_data(data)
    report_summary = get_report_summary(data, associated_programs)
        
    return columns, data, None, chart, report_summary

def get_associated_programs():
    current_user = frappe.session.user
    user_data = frappe.db.sql("""
        SELECT 
            e.custom_program,
            p.custom_head_of_department_user_id,
            p.custom_portfolio_coordinator_user_id
        FROM 
            tabEmployee e
        JOIN 
            tabProgram p
        ON 
            e.custom_program = p.program_name
        WHERE 
            e.user_id = %s
    """, (current_user,), as_dict=True)

    if not user_data:
        return []

    user_roles = user_data[0]
    if current_user in [user_roles.custom_head_of_department_user_id, user_roles.custom_portfolio_coordinator_user_id]:
        return [user_roles.custom_program]
    
    return []

def get_columns():
    return [
        {
            "fieldname": "ipr",
            "label": _("IPR"),  # Ensure to use `_` here
            "fieldtype": "Link",
            "options": "IPR Type",
            'width': '120'
        },
        {
            "fieldname": "academic_year",
            "label": _("Academic Year"),
            "fieldtype": "Link",
            "options": "Academic Year",
            'width': '170'
        },
        {
            "fieldname": "filed_date",
            "label": _("Field Date"),
            "fieldtype": "Date",
            'width': '170'
        },
        {
            "fieldname": "instructors",
            "label": _("Instructors"),
            "fieldtype": "Link",
            "options": "Instructor",  # Corrected typo here
            'width': '170'
        },
        {
            "fieldname": "employee_id",
            "label": _("Employee ID"),
            "fieldtype": "Data",
            'width': '120'
        },
        {
            "fieldname": "program",
            "label": _("Program"),
            "fieldtype": "Link",
            "options": "Program",  # Corrected typo here
            'width': '120'
        },
        {
            "fieldname": "affiliation",
            "label": _("Affiliation"),
            "fieldtype": "Data",
            'width': '120'
        },
        {
            "fieldname": "finacial_year",  # Corrected typo here
            "label": _("Financial Year"),
            "fieldtype": "Link",
            "options": "Fiscal Year",
            'width': '120'
        },
        {
            "fieldname": "title",
            "label": _("Title"),
            "fieldtype": "Data",
            'width': '120'
        },
        {
            "fieldname": "application_no",
            "label": _("Application / Diary No."),
            "fieldtype": "Data",
            'width': '120'
        },
        {
            "fieldname": "published_date_or_granted_date",
            "label": _("Published Date or Granted Date"),
            "fieldtype": "Date",
            'width': '120'
        },
        {
            "fieldname": "status",
            "label": _("Status"),  # Corrected typo here
            "fieldtype": "Select",
            'width': '120'
        },
        {
            "fieldname": "publication_number_or_granted_number",
            "label": _("Publication Number or Granted Number"),
            "fieldtype": "Data",
            'width': '120'
        },
        {
            "fieldname": "registration_no",
            "label": _("Registration No"),
            "fieldtype": "Data",
            'width': '120'
        },
        {
            "fieldname": "status_of_ipr",
            "label": _("Status of IPR"),
            "fieldtype": "Select",
            'width': '120'
        }
    ]

def get_cs_data(filters, associated_programs):
    conditions = get_conditions(filters, associated_programs)
    data = frappe.get_all(
        doctype='IPR',
        fields=[
            'ipr', 'academic_year', 'filed_date', 'instructors', 'employee_id', 'program', 
            'affiliation', 'finacial_year', 'title', 'application_no', 'published_date_or_granted_date', 
            'status', 'publication_number_or_granted_number', 'registration_no', 'status_of_ipr', 'attachment'
        ],
        filters=conditions
    )
    return data

def get_conditions(filters, associated_programs):
    conditions = {}
    for key, value in filters.items():
        if value:
            conditions[key] = value

    if associated_programs:
        conditions['program'] = ['in', associated_programs]

    return conditions

def get_chart_data(data):
    if not data:
        return None

    labels = set(entry.program for entry in data)
    sub_labels = set(entry.ipr for entry in data)

    data_dict = {label: {sub_label: 0 for sub_label in sub_labels} for label in labels}

    for entry in data:
        if entry.status == "Approved":
            program = entry.program
            ipr = entry.ipr
            data_dict[program][ipr] += 1

    datasets = []

    for sub_label in sub_labels:
        dataset = {
            'name': sub_label,
            'values': [],
        }
        for label in labels:
            dataset['values'].append(data_dict[label][sub_label])
        datasets.append(dataset)

    chart = {
        'data': {
            'labels': list(labels),
            'datasets': datasets
        },
        'type': 'bar',
        'height': 10,
        'width': 10,
    }
    return chart

def get_report_summary(data, associated_programs):
    if not data:
        return None

    all_programs_set = set(associated_programs) if associated_programs else set()

    if not associated_programs:
        all_programs = frappe.get_all(
            doctype='Program',
            fields=['program_name']
        )
        all_programs_set = {entry.program_name for entry in all_programs}

    program_counts = {program: 0 for program in all_programs_set}

    for entry in data:
        if entry.status in {"Approved"}:
            if entry.program in program_counts:
                program_counts[entry.program] += 1

    summary_data = []

    for program, count in program_counts.items():
        summary_data.append({
            'value': count,
            'indicator': 'Green',
            'label': program,
            'datatype': 'Int',
            'width': '20',
        })

    return summary_data

@frappe.whitelist()
def log_current_user_data():
    current_user = frappe.session.user
    result = frappe.db.sql("""
        SELECT 
            e.employee,
            e.custom_program,
            e.user_id,
            e.employee_name,
            p.custom_head_of_department_user_id,
            p.custom_portfolio_coordinator_user_id
        FROM 
            tabEmployee e
        JOIN 
            tabProgram p
        ON 
            e.custom_program = p.program_name
        WHERE 
            e.user_id = %s
    """, (current_user,), as_dict=True)

    return result