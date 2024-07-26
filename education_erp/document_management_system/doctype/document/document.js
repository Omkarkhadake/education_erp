
// User Permission wokring Correct

frappe.ui.form.on("Document", {
    onload: function (frm) {
        if (!frm.is_new() && frm.doc.docstatus === 1 && frm.doc.status === "Approved" && frm.doc.user_access_profile =="Confidential") {
            // Check if the current user is in the allowed users list
            let allowed_users = frm.doc.allowed_users.map(user => user.dms_user_access);
            if (!allowed_users.includes(frappe.session.user)) {
                frappe.msgprint(__('You do not have permission to access this document.'));
                frappe.set_route('List', 'Document');
                return;
            }
        }

        if (frm.is_new()) {
            frm.set_value('document_creation_date', frappe.datetime.nowdate());
            frm.set_intro('Upload New Document');

            frappe.call({
                method: "education_erp.document_management_system.doctype.document.document.get_user_mail_id",
                args: { user: frappe.session.user },
                callback: function (response) {
                    if (response.message) {
                        const { email, employee_id, employee_name, designation } = response.message;
                        frm.set_value({
                            'employee': employee_id,
                            'email_id': email,
                            'employee_name': employee_name,
                            'designation': designation
                        });
                    } else {
                        frappe.msgprint("Email ID not found or error occurred.");
                    }
                },
                error: function (xhr, status, error) {
                    frappe.msgprint("Error fetching user's email ID.");
                    console.error("Error fetching user's email ID:", error);
                }
            });
        }
    },

    refresh: function (frm) {
        if (!frm.is_new() && frm.doc.docstatus === 1 && frm.doc.status === "Approved") {
            // Ensure the current user can edit the document if they are in the allowed users list
            let allowed_users = frm.doc.allowed_users.map(user => user.dms_user_access);
            if (!allowed_users.includes(frappe.session.user)) {
                frm.disable_form();
            }
        }

        frm.set_query('document_sub_category', function (doc) {
            return { filters: { document_category: doc.document_category } };
        });

        frm.set_query('document_types', function (doc) {
            return { filters: { document_sub_category: doc.document_sub_category } };
        });

        frm.remove_custom_button(__('Approve'));
        frm.remove_custom_button(__('Reject'));

        if (frm.doc.status === 'Pending' && frappe.session.user === frm.doc.approving_authority_id) {
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

        if (frm.doc.docstatus === 1 && frm.doc.status === "Approved") {
            frm.add_custom_button(__("Request for this document"), function () {
                frappe.confirm(`Are you sure you want to request "${frm.doc.document_name}" ?`, function () {
                    const documentId = frm.doc.name;

                    if (documentId) {
                        frappe.call({
                            method: "education_erp.document_management_system.doctype.document.document.get_document_details",
                            args: { doc_id: documentId },
                            callback: function (response) {
                                if (response.message) {
                                    checkDocumentAvailability(response.message);
                                } else {
                                    frappe.msgprint("Document not found or error occurred.");
                                }
                            },
                            error: function (xhr, status, error) {
                                frappe.msgprint("Error fetching document details. Please try again.");
                                console.error("Error fetching document details:", error);
                            }
                        });
                    } else {
                        frappe.msgprint("Document ID is empty.");
                    }
                });
            });
        }
    },

    document_category: function (frm) {
        frm.set_query('document_sub_category', function (doc) {
            return { filters: { document_category: doc.document_category } };
        });
    },

    document_sub_category: function (frm) {
        frm.set_query('document_types', function (doc) {
            return { filters: { document_sub_category: doc.document_sub_category } };
        });
    },

    on_submit: function (frm) {
        frm.set_value('status', 'Pending');
        frm.save_or_update();
    },
});

function checkDocumentAvailability(documentDetails) {
    frappe.call({
        method: "education_erp.document_management_system.doctype.document.document.get_movement_of_document_list",
        args: { doc_id: documentDetails.name },
        callback: function (response) {
            if (response.message.length > 0) {
                let today = frappe.datetime.get_today();
                let documentAllocated = false;
                let toDate;

                response.message.forEach(function (record) {
                    if ((today >= record.document_start_date && today <= record.document_end_date) || record.status === "Returned") {
                        documentAllocated = true;
                        toDate = record.document_end_date;
                    }
                });

                if (documentAllocated) {
                    frappe.msgprint(`Given Document is already allocated, and it's available after "${toDate}".`);
                } else {
                    routeToMovementOfOriginalDocument(documentDetails);
                }
            } else {
                routeToMovementOfOriginalDocument(documentDetails);
            }
        }
    });
}

function routeToMovementOfOriginalDocument(documentDetails) {
    frappe.model.with_doctype('Movement of Original Document', function () {
        let doc = frappe.model.get_new_doc('Movement of Original Document');
        Object.assign(doc, {
            document_name: documentDetails.document_name,
            document_number: documentDetails.document_number,
            default_custodian: documentDetails.custodian_of_original_document,
            default_custodian_email: documentDetails.custodian_email
        });
        frappe.set_route("Form", "Movement of Original Document", doc.name);
    });
}

