// Copyright (c) 2024, ppcrc and contributors
// For license information, please see license.txt

frappe.query_reports["Task Summary"] = {
	filters: [
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
		},
		{
			fieldname: "priority",
			label: __("Priority"),
			fieldtype: "Select",
			options: ["", "Low", "Medium", "High", "Urgent"],
		},
		{
			fieldname: "task_frequency",
			label: __("Task Frequency"),
			fieldtype: "Select",
			options: ["", "One-time", "Yearly", "Half-yearly", "Quarterly","Bi-monthly","Monthly","Fortnightly","Weekly"],
		},
		{
			fieldname: "status",
			label: __("Status"),
			fieldtype: "Select",
			options: ["", "Open", "Not Started", "On Hold", "Closed", "Pending","Rejected","Completed"],
		},
		{
			fieldname: "task_category",
			label: __("Task Category"),
			fieldtype: "Link",
			options: "Task Category",
		},
		{
			fieldname: "regulating_authority",
			label: __("Regulating Authority"),
			fieldtype: "Link",
			options: "Regulating Authority",
		},
		{
			fieldname: "Task Sub-Category",
			label: __("Task Sub-Category"),
			fieldtype: "Link",
			options: "Task Sub-Category",
		},
		{
			fieldname: "task_name",
			label: __("Task Name"),
			fieldtype: "Link",
			options: "Task Name",
		},
	],
	formatter: function (value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (column.id == "delay") {
			if (data["delay"] > 0) {
				value = `<p style="color: red; font-weight: bold">${value}</p>`;
			} else {
				value = `<p style="color: green; font-weight: bold">${value}</p>`;
			}
		}
		return value;
	},
};