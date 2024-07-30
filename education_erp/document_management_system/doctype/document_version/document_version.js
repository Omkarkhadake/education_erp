// Copyright (c) 2024, ppcrc and contributors
// For license information, please see license.txt

frappe.ui.form.on("Document Version", {
    onload: function(frm) {
        console.log("running.........");
        if (frm.is_new()) {
            frm.set_intro('Create New Document Version');
        }
    },
    on_submit: function(frm) {
        frm.set_value('status', 'Pending');
        frm.save_or_update();
    },
 
    refresh: function (frm) {
        frm.remove_custom_button(__('Approve'));
        frm.remove_custom_button(__('Reject'));

        if (frm.doc.status === 'Pending' && frappe.session.user === frm.doc.approving_authority) {
            frm.add_custom_button(__('Approve'), function () {
                frappe.confirm(`Are you sure you want to approve "${frm.doc.document_name}" ?`, function () {
                    frm.call('approve').then(() => { frm.reload_doc(); });
                });
            }, __("Action"));

            frm.add_custom_button(__('Reject'), function () {
                frappe.confirm(`Are you sure you want to reject "${frm.doc.document_name}" ?`, function () {
                    frm.call('reject').then(() => { frm.reload_doc(); });
                });
            }, __("Action"));
        }

    },

    },
);
