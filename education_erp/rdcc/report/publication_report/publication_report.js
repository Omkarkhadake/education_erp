

frappe.query_reports["Publication Report"] = {
    "filters": [
        {
            "fieldname": "publication",
            "label": __("Publication"),
            "fieldtype": "Link",
            "options": "Publication Type"
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
            "fieldname": "date_of_publication",
            "label": __("Publication Date Range"),
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
    ],
    onload: function(report) {
        log_current_user_data();
    }
};

function log_current_user_data() {
    frappe.call({
        method: "education_erp.rdcc.report.publication_report.publication_report.log_current_user_data",
        callback: function(r) {
            if (r.message) {
                console.log("Current User Data: ", r.message[0]);
            } else {
                console.error("Error retrieving user data: ", r);
            }
        }
    });
}