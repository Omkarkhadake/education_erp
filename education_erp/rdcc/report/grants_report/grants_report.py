
import frappe
from frappe import _, msgprint

def execute(filters=None):
    associated_programs = get_associated_programs()
    if not filters:
        filters = {}

    if filters.get('date_of_award'):
        start_date = filters['date_of_award'][0]
        end_date = filters['date_of_award'][1]
        filters['date_of_award'] = ["between", (start_date, end_date)]

    data, columns = [], []
    columns = get_columns()  # Populate the columns list
    cs_data = get_cs_data(filters, associated_programs)

    if not cs_data:
        msgprint(_('No Records Found'))
        return columns, cs_data, None, None, None

    data = []
    for d in cs_data:
        row = frappe._dict({
            'grant': d.grant,
            'instructor': d.instructor,
            'academic_year': d.academic_year,
            'fiscal_year': d.fiscal_year,
            'employee_id': d.employee_id,
            'program': d.program,
            'name_of_the_principal_investigator': d.name_of_the_principal_investigator,
            'name_of_project': d.name_of_project,
            'amount_sanctioned': d.amount_sanctioned,
            'name_of_the_funding_agency': d.name_of_the_funding_agency,
            'status': d.status,
            'department_of_principal_investigator': d.department_of_principal_investigator,
            'date_of_award': d.date_of_award,
            'duration_of_the_project': d.duration_of_the_project,
            'research_type': d.research_type,
            'attachment': d.attachment,
            'grants_status':d.grants_status,
            'start_date':d.start_date,
            'end_date':d.end_date
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
            "fieldname": "grant",
            "label": _("Grant"),
            "fieldtype": "Link",
            "options": "Grants Type"
        },
        {
            "fieldname": "program",
            "label": _("Program"),
            "fieldtype": "Link",
            "options": "Program",
            'width': '170'
        },
        {
            "fieldname": "instructor",
            "label": _("Instructor"),
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
            "fieldname": "date_of_award",
            "label": _("Date of Awaed"),
            "fieldtype": "Date",
            'width': '120'
        },
        {
            "fieldname": "start_date",
            "label": _("start_date"),
            "fieldtype": "Date",
            'width': '120'
        },
        {
            "fieldname": "end_date",
            "label": _("End Date"),
            "fieldtype": "Date",
            'width': '120'
        },
        {
            "fieldname": "name_of_project",
            "label": _("Name of Project"),
            "fieldtype": "Data",
            'width': '120'
        },
        {
            "fieldname": "fiscal_year",
            "label": _("Financial Year"),
            "fieldtype": "Link",
            "options": "Fiscal Year",
            'width': '120'
        },
        {
            "fieldname": "name_of_the_principal_investigator",
            "label": _("Name of Principal investigator"),
            "fieldtype": "Data",
            'width': '120'
        },
        {
            "fieldname": "research_type",
            "label": _("Research Type"),
            "fieldtype": "Select",
            'width': '120'
        },
        {
            "fieldname": "department_of_principal_investigator",
            "label": _("Department of Principal Investigator"),
            "fieldtype": "Data",
            'width': '120'
        },
        {
            "fieldname": "amount_sanctioned",
            "label": _("Amount Sanctioned"),
            "fieldtype": "Currency",
            'width': '120'
        },
        {
            "fieldname": "duration_of_the_project",
            "label": _("Duration of the Project"),
            "fieldtype": "Data",
            'width': '120'
        },
        {
            "fieldname": "name_of_the_funding_agency",
            "label": _("Name of The Funcding Agency"),
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
            "fieldname": "grants_status",
            "label": _("Grants Status"),
            "fieldtype": "Data",
            'width': '120'            
        },
        {
            "fieldname": "attachment",
            "label": _("Attachment"),
            "fieldtype": "Data",
            'width': '120'
        }
    ]


def get_cs_data(filters, associated_programs):
    conditions = get_conditions(filters, associated_programs)
    data = frappe.get_all(
        doctype='Grant',
        fields=[
            'grant',  'instructor', 'academic_year', 'fiscal_year', 'employee_id', 
            'program', 'name_of_the_principal_investigator', 'department_of_principal_investigator', 'name_of_project', 'date_of_award', 
            'amount_sanctioned', 'name_of_the_funding_agency', 'research_type', 'status', 'attachment','grants_status','start_date','end_date'
        ],
        filters=conditions
    )
    return data

def get_conditions(filters, associated_programs):
    conditions = {}
    for key, value in filters.items():
        if filters.get(key):
            conditions[key] = value

    if associated_programs:
        conditions['program'] = ['in', associated_programs]

    return conditions

def get_chart_data(data):
    if not data:
        return None

    labels = set(entry.program for entry in data)
    sub_labels = set(entry.grant for entry in data)

    data_dict = {label: {sub_label: 0 for sub_label in sub_labels} for label in labels}

    for entry in data:
        if entry.status == "Approved":
            program = entry.program
            grant = entry.grant
            data_dict[program][grant] += 1

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

    # Get all grant types
    all_grant_types = frappe.get_all(
        doctype='Grants Type',
        fields=['grants_type']
    )
    all_grant_types_set = {entry.grants_type for entry in all_grant_types}

    # Filter data for approved entries
    approved_data = [entry for entry in data if entry.status == "Approved"]

    # Initialize dictionary for amounts
    grant_type_amounts = {grant: 0 for grant in all_grant_types_set}

    # Calculate amounts
    for entry in approved_data:
        if entry.grant in grant_type_amounts:
            grant_type_amounts[entry.grant] += entry.amount_sanctioned

    # Create summary data
    summary_data = []

    # Add summary for total amount sanctioned with box-like structure
    summary_data.append({
        'value': sum(grant_type_amounts.values()),
        'indicator': 'Red',
        'label': 'Total Amount Sanctioned',
        'datatype': 'Currency',
        'width': '10',
        'css_style': 'border: 1px solid black; padding: 5px;',  # CSS style for the box-like structure
    })

    # Add separator
    summary_data.append({
        'value': '=',
        'label': '',
        'datatype': 'Data',
        'width': '1',
    })

    # Add summary for each grant type's total amount sanctioned
    for grant_type, amount in grant_type_amounts.items():
        summary_data.append({
            'value': amount,
            'indicator': 'Red',
            'label': grant_type,
            'datatype': 'Currency',
            'width': '10',
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




