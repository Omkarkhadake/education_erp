
//  autoupdate from when ever action perform
// now_datetime for Date of Receiver ans Date of Returned

frappe.ui.form.on('Movement of Original Document', {
    onload: function(frm) {
        // Set date_of_movement to today's date
        frm.set_value('date_of_movement', frappe.datetime.nowdate());

        // Fetch current user's email and employee ID
        getUserDetails(frm);

        // Fetch document details if document ID is present
        if (frm.doc.document) {
            getDocumentDetails(frm, frm.doc.document);
        }

        if (frm.is_new()) {
            frm.set_intro('Create New Movement of Original Document');
        }
    },

    on_submit: function(frm) {
        // Set status to 'Pending For Approver' after form is submitted
        frm.set_value('status', 'Pending');
        frm.save_or_update();
    },
    

    refresh: function(frm) {
        // Remove existing custom buttons if necessary
        frm.remove_custom_button(__('Approve'));
        frm.remove_custom_button(__('Reject'));

        let default_custodian_email = frm.doc.default_custodian_email;

        if (frm.doc.status === 'Pending' && frappe.session.user === default_custodian_email) {
            addApproveRejectButtons(frm);
        }



        if (frm.doc.status === 'Approved' && frappe.session.user === frm.doc.owner) {
            // Add Received button
            frm.add_custom_button(__('Received'), function() {
                frappe.confirm('Are you sure you want to mark this document as Received?', function() {
                    frm.call('received').then(() => {
                        frm.set_value('date_of_received', frappe.datetime.now_datetime());
                        frm.save('Update');
                        // frappe.msgprint(`New Field Recipient Date "${frappe.datetime.nowdate()}" is added, Kindly click on Update Button to Save Changes.`);
                    });
                });
            }, __("Action"));
        }



        if (frm.doc.status === 'Received' && frappe.session.user === default_custodian_email) {
            // Add Returned button
            frm.add_custom_button(__('Returned'), function() {
                frappe.confirm('Are you sure you want to mark this document as returned?', function() {
                    frm.call('received_back').then(() => {
                        frm.set_value('date_of_document_returned_to_custodian', frappe.datetime.now_datetime());
                        frm.save('Update');
                    });
                });
            }, __("Action"));
        }

    }
});

function getUserDetails(frm) {
    frappe.call({
        method: "education_erp.document_management_system.doctype.movement_of_original_document.movement_of_original_document.get_user_mail_id",
        args: { user: frappe.session.user },
        callback: function(response) {
            if (response.message) {
                if (frm.doc.__islocal) {
                    // Set document_receiver only if the document is new
                    // frm.set_value('document_receiver', response.message.employee_id);
                }
            } else {
                frappe.msgprint("User details not found.");
            }
        },
        error: function(err) {
            frappe.msgprint("Error fetching user details: " + err);
        }
    });
}

function getDocumentDetails(frm, doc_id) {
    frappe.call({
        method: "education_erp.document_management_system.doctype.document.document.get_document_details",
        args: { doc_id: doc_id },
        callback: function(response) {
            if (response.message) {
                frm.set_value('document_name', response.message.document_name);
                frm.set_value('document_number', response.message.document_number);
                frm.set_value('default_custodian', response.message.custodian_of_original_document);
                frm.set_value('custodian_email', response.message.default_custodian_email);
            } else {
                frappe.msgprint("Document details not found.");
            }
        },
        error: function(err) {
            frappe.msgprint("Error fetching document details: " + err);
        }
    });
}

function addApproveRejectButtons(frm) {
    frm.add_custom_button(__('Approve'), function() {
        frappe.confirm('Are you sure you want to approve this document?', function() {
            frm.call('approve').then(() => {
                frm.set_value('approval_date', frappe.datetime.nowdate());
                frm.save('Update'); // Save after approval
            });
        });
    }, __("Action"));

    frm.add_custom_button(__('Reject'), function() {
        frappe.confirm('Are you sure you want to reject this document?', function() {
            frm.call('reject').then(() => {
                frm.reload_doc();
                frm.save();
            });
        });
    }, __("Action"));
}

