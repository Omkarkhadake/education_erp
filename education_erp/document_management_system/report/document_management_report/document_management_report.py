import frappe
from frappe import _, msgprint

def execute(filters=None):
    if not filters:
        filters = {}
    if filters.get('document_creation_date'):
        start_date = filters['document_creation_date'][0]
        end_date = filters['document_creation_date'][1]
        filters['document_creation_date'] = ["between", (start_date, end_date)]
    
    data, columns = [], []
    
    columns = get_columns()
    cs_data = get_cs_data(filters)
    
    if not cs_data:
        msgprint(_('No Records Found'))
        return columns, cs_data, None, None, None
    
    data = []
    for d in cs_data:
        row = frappe._dict({
            'entity_name': d.entity_name,
            'fiscal_year': d.fiscal_year,
            'document_creation_date': d.document_creation_date,
            'employee': d.employee,
            'designation': d.designation,
            'employee_name': d.employee_name,
            'email_id': d.email_id,
            'government_bodies_and_regulators': d.government_bodies_and_regulators,
            'document_category': d.document_category,
            'approving_authority_id': d.approving_authority_id,
            'document_sub_category': d.document_sub_category,
            'document_name': d.document_name,
            'document_number': d.document_number,
            'document_date': d.document_date,
            'application_number': d.application_number,
            'custodian_of_original_document': d.custodian_of_original_document,
            'custodian_email': d.custodian_email,
            'document_format': d.document_format,
            'document_access_profile': d.document_access_profile,
            'document_types': d.document_types,
            'document_status': d.document_status,
            'document_source': d.document_source,
            'document_start_date': d.document_start_date,
            'document_end_date': d.document_end_date,
            'website_reference': d.website_reference,
            'remarks': d.remarks,
            'status': d.status   
        })
        data.append(row)
        
    return columns, data, None, None, None

def get_columns():
    return [
        {
            "fieldname": "entity_name",
            "label": _("Entity Name"),
            "fieldtype": "Link",
            "options": "Company",
            'width': '120'
        },
        {
            "fieldname": "fiscal_year",
            "label": _("Fiscal Year"),
            "fieldtype": "Link",
            "options": "Fiscal Year",
            'width': '170'
        },
        {
            "fieldname": "employee",
            "label": _("Employee"),
            "fieldtype": "Link",
            "options": "Employee",
            'width': '170'
        },
        {
            "fieldname": "designation",
            "label": _("Designation"),
            "fieldtype": "Data",
            'width': '170'
        },
        {
            "fieldname": "document_creation_date",
            "label": _("Document Creation Date"),
            "fieldtype": "Date",
            'width': '120'
        },
        {
            "fieldname": "employee_name",
            "label": _("Employee Name"),
            "fieldtype": "Data",
            'width': '120'
        },
        {
            "fieldname": "email_id",
            "label": _("Email-id"),
            "fieldtype": "Data",
            'width': '120'
        },
        {
            "fieldname": "government_bodies_and_regulators",
            "label": _("Government Bodies and Regulators"),
            "fieldtype": "Link",
            "options": "Government bodies and Regulators",
            'width': '120'
        },
        {
            "fieldname": "document_category",
            "label": _("Document Category"),
            "fieldtype": "Link",
            "options": "Document Category",
            'width': '120'
        },
        {
            "fieldname": "approving_authority_id",
            "label": _("Approving Authority Id"),
            "fieldtype": "Link",
            "options": "User",
            'width': '120'
        },
        {
            "fieldname": "document_sub_category",
            "label": _("Document Sub-Category"),
            "fieldtype": "Link",
            "options": "Document Sub-Category",
            'width': '120'
        },
        {
            "fieldname": "document_name",
            "label": _("Document Name"),
            "fieldtype": "Link",
            "options": "Document Name",
            'width': '120'
        },
        {
            "fieldname": "document_number",
            "label": _("Document Number"),
            "fieldtype": "Data",
            'width': '120'
        },
        {
            "fieldname": "document_date",
            "label": _("Document Date"),
            "fieldtype": "Date",
            'width': '120'
        },
        {
            "fieldname": "application_number",
            "label": _("Application Number"),
            "fieldtype": "Data",
            'width': '120'
        },
        {
            "fieldname": "custodian_of_original_document",
            "label": _("Custodian of Original Document"),
            "fieldtype": "Link",
            "options": "Employee",
            'width': '120'
        },
        {
            "fieldname": "custodian_email",
            "label": _("Custodian Email"),
            "fieldtype": "Data",
            'width': '120'
        },
        {
            "fieldname": "document_format",
            "label": _("Document Format"),
            "fieldtype": "Select",
            "options": "",
            'width': '120'
        },
        {
            "fieldname": "document_access_profile",
            "label": _("Document Access Profile"),
            "fieldtype": "Select",
            "options": "",
            'width': '120'
        },
        {
            "fieldname": "document_types",
            "label": _("Document Types"),
            "fieldtype": "Data",
            "options": "",
            'width': '120'
        },
        {
            "fieldname": "document_status",
            "label": _("Document Status"),
            "fieldtype": "Select",
            "options": "",
            'width': '120'
        },
        {
            "fieldname": "status",
            "label": _("Status"),
            "fieldtype": "Data",
            'width': '120'
        },
        {
            "fieldname": "document_source",
            "label": _("Document Source"),
            "fieldtype": "Link",
            "options": "Document Source",
            'width': '120'
        },
        {
            "fieldname": "document_start_date",
            "label": _("Document Start Date"),
            "fieldtype": "Date",
            'width': '120'
        },
        {
            "fieldname": "document_end_date",
            "label": _("Document End Date"),
            "fieldtype": "Date",
            'width': '120'
        },
        {
            "fieldname": "website_reference",
            "label": _("Website Reference"),
            "fieldtype": "Link",
            "options": "Website Reference",
            'width': '120'
        },
        {
            "fieldname": "remarks",
            "label": _("Remarks"),
            "fieldtype": "Data",
            'width': '120'
        }
    ]

def get_cs_data(filters):
    conditions = get_conditions(filters)
    data = frappe.get_all(
        doctype='Document',
        fields=[
            'entity_name', 'fiscal_year', 'employee', 'designation', 'document_creation_date', 'employee_name', 
            'email_id', 'government_bodies_and_regulators', 'document_category', 'approving_authority_id', 'document_sub_category', 
            'document_name', 'document_number', 'document_date', 'status', 'application_number',
            'custodian_of_original_document', 'custodian_email', 'document_format', 'document_access_profile', 'document_types',
            'document_status', 'document_source', 'document_start_date', 'document_end_date', 'website_reference', 'remarks'
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