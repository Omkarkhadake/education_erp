// Copyright (c) 2024, ppcrc and contributors
// For license information, please see license.txt

frappe.query_reports["Awards and Recognition Report"] = {
	"filters": [
        {
            "fieldname": "program",
            "label": __("Select Program"),
            "fieldtype": "Link",
            "options": "Program"
        },
        {
            "fieldname": "instructor",
            "label": __("Instructor"),
            "fieldtype": "Link",
            "options": "Instructor"
        },
        {
            "fieldname": "status",
            "label": __("Status"),
            "fieldtype": "Select",
            "options": "\nDraft\nPending\nApproved\nRejected"
        },
        {
            "fieldname": "award_date",
            "label": __("Award Date"),
            "fieldtype": "DateRange"
        },
        {
            "fieldname": "academic_year",
            "label": __("Academic Year"),
            "fieldtype": "Link",
            "options": "Academic Year"
        },
        {
            "fieldname": "financial_year",
            "label": __("Financial Year"),
            "fieldtype": "Link",
            "options": "Fiscal Year"
        }
    ]

};