// Copyright (c) 2024, ppcrc and contributors
// For license information, please see license.txt

frappe.query_reports["Document Management Report"] = {
	"filters": [
		{
            "fieldname": "entity_name",
            "label": __("Entity Name"),
            "fieldtype": "Link",
            "options": "Company"
        },
		{
            "fieldname": "government_bodies_and_regulators",
            "label": __("Government Bodies and Regulators"),
            "fieldtype": "Link",
            "options": "Government Bodies and Regulators"
        },
		{
            "fieldname": "document_category",
            "label": __("Document Category"),
            "fieldtype": "Link",
            "options": "Document Category"
        },
		{
            "fieldname": "document_sub_category",
            "label": __("Document Sub-Category"),
            "fieldtype": "Link",
            "options": "Document Sub-Category"
        },
		{
            "fieldname": "document_types",
            "label": __("Document Types"),
            "fieldtype": "Link",
            "options": "Document Types"
        },
		{
            "fieldname": "status",
            "label": __("Doctype Status"),
            "fieldtype": "Select",
            "options": "\nDraft\nPending\nApproved\nRejected"
        },
        {
            "fieldname": "user_access_profile",
            "label": __("User Access Profile"),
            "fieldtype": "Select",
            "options": "\nPublic\nConfidential"
        },
		{
            "fieldname": "document_status",
            "label": __("Document Status"),
            "fieldtype": "Select",
            "options": "\nDraft\nPending\nFinal"
        },
		{
            "fieldname": "fiscal_year",
            "label": __("Fiscal Year"),
            "fieldtype": "Link",
            "options": "Fiscal Year"
        },
		{
            "fieldname": "document_creation_date",
            "label": __("Document Creation Date"),
            "fieldtype": "DateRange"
        },

	]
};