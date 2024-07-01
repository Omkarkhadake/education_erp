// Copyright (c) 2024, ppcrc and contributors
// For license information, please see license.txt

frappe.query_reports["IPR Report"] = {
	"filters": [
		{
            "fieldname": "ipr",
            "label": __("IPR"),
            "fieldtype": "Link",
            "options": "IPR Type"
        },
        {
            "fieldname": "academic_year",
            "label": __("Academic Year"),
            "fieldtype": "Link",
            "options": "Academic Year"
        },
        {
            "fieldname": "filed_date",
            "label": __("Filed Date"),
            "fieldtype": "DateRange"
        },
        {
            "fieldname": "instructors",
            "label": __("Instructors"),
            "fieldtype": "Link",
            "options": "Instructor"

        },
        {
            "fieldname": "program",
            "label": __("Program"),
            "fieldtype": "Link",
            "options": "Program"

        },
        {
            "fieldname": "finacial_year",
            "label": __("Finacial Year"),
            "fieldtype": "Link",
            "options": "Fiscal Year"
        },
        {
            "fieldname": "status",
            "label": __("Status"),
            "fieldtype": "Select",
            "options": "\nDraft\nPending\nApproved\nRejected"
        }
	]
};

function log_current_user_data() {
    frappe.call({
        method: "education_erp.rdcc.report.ipr_report.ipr_report.log_current_user_data",
        callback: function(r) {
            if (r.message) {
                console.log("Current User Data: ", r.message[0]);
            } else {
                console.error("Error retrieving user data: ", r);
            }
        }
    });
}