# Copyright (c) 2024, omkar and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class MovementofOriginalDocument(Document):
    @frappe.whitelist()
    def on_submit(self, new_status="Pending"):
        self.status = new_status
        self.save()

    @frappe.whitelist()
    def approve(self):
        self.status = "Approved"
        self.save()

    @frappe.whitelist()
    def reject(self):
        self.status = "Rejected"
        self.save()

    @frappe.whitelist()
    def received(self):
        self.status = "Received"
        self.save()

    @frappe.whitelist()
    def received_back(self):
        self.status = "Returned"
        self.save()

@frappe.whitelist()
def get_user_mail_id(user=None):
    try:
        # Get the email of the user based on the user ID
        email = frappe.db.get_value("User", user, "email")
        # Fetch Employee ID based on the User ID
        employee_id = frappe.db.get_value("Employee", {"user_id": user}, "name")
        return {
            "email": email,
            "employee_id": employee_id
        }
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Failed to fetch user details")
        return None


import frappe
from frappe.model.document import Document

@frappe.whitelist()
def get_movement_details(doc_id):
    try:
        # Fetch document details based on the document ID
        doc = frappe.get_doc("Movement of Original Document", doc_id)
        # Extract relevant details and return as a dictionary
        return {
            "document_name": doc.document_name,
            "document_number": doc.document_number,
            "custodian_of_original_document": doc.custodian_of_original_document,
            "default_custodian_email": doc.default_custodian_email
        }
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Failed to fetch document details")
        return None

