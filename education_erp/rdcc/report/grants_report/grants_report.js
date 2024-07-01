// Copyright (c) 2024, ppcrc and contributors
// For license information, please see license.txt

frappe.query_reports["Grants Report"] = {
	"filters": [

		{
            "fieldname": "grant",
            "label": __("Grant"),
            "fieldtype": "Link",
            "options": "Grants Type"
        },
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
            "fieldname": "grants_status",
            "label": __("Grants Status"),
            "fieldtype": "Select",
            "options": "\nOngoing\nCompleted"
        },
        {
            "fieldname": "academic_year",
            "label": __("Academic Year"),
            "fieldtype": "Link",
            "options": "Academic Year"
        },
        {
            "fieldname": "fiscal_year",
            "label": __("Financial Year"),
            "fieldtype": "Link",
            "options": "Fiscal Year"
        },
		{
            "fieldname": "date_of_award",
            "label": __("Date of Award"),
            "fieldtype": "DateRange"
        }

	],
    onload: function(report) {
        log_current_user_data();
    }
};

function log_current_user_data() {
    frappe.call({
        method: "education_erp.rdcc.report.grants_report.grants_report.log_current_user_data",
        callback: function(r) {
            if (r.message) {
                console.log("Current User Data: ", r.message[0]);
            } else {
                console.error("Error retrieving user data: ", r);
            }
        }
    });
}