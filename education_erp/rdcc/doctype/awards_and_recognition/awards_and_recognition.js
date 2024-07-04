// Copyright (c) 2024, ppcrc and contributors
// For license information, please see license.txt
frappe.ui.form.on("Awards and Recognition", {
    onload: function (frm) {
        console.log("running.........");
        if (frm.is_new()) {
            frm.set_intro('Create New Awards and Recognition Doctype');
        }
    },
    on_submit: function (frm) {
        frm.set_value('status', 'Pending');
        frm.save_or_update();
    },
    refresh: function (frm) {
        // Remove existing custom buttons
        frm.remove_custom_button(__('Approve'));
        frm.remove_custom_button(__('Reject'));

        // Check if the document status is 'Pending'
        if (frm.doc.status === 'Pending') {
            // Call get_instructor_program_details to get the necessary details
            frappe.call({
                method: "education_erp.rdcc.doctype.awards_and_recognition.awards_and_recognition.get_instructor_program_details",
                callback: function (response) {
                    if (response.message) {
                        console.log("response: ", response.message);
                        console.log("current user: ", frappe.session.user);

                        // Check if the current user matches the head of department or portfolio coordinator
                        let userIsAuthorized = response.message.some(item =>
                            frappe.session.user === item.custom_head_of_department_user_id ||
                            frappe.session.user === item.custom_portfolio_coordinator_user_id
                        );

                        // If the user is authorized, add Approve and Reject buttons
                        if (userIsAuthorized) {
                            frm.add_custom_button(__('Approve'), function () {
                                frm.call('approve').then(() => {
                                    frappe.msgprint(`${frm.doc.employee_id}-${frm.doc.instructor}  Approved`);
                                    frm.reload_doc();
                                    frm.save();
                                });
                            }, __("Action"));

                            frm.add_custom_button(__('Reject'), function () {
                                frm.call('reject').then(() => {
                                    frappe.msgprint(`${frm.doc.employee_id}-${frm.doc.instructor}  Rejected`);
                                    frm.reload_doc();
                                    frm.save();
                                });
                            }, __("Action"));
                        }
                    }
                }
            });
        }
    },
    after_cancel: function (frm) {
        frm.set_value('status', 'Cancelled');
        frm.save_or_update();
    },
});
