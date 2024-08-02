# # Copyright (c) 2024, ppcrc and contributors
# # For license information, please see license.txt

# import frappe
# from frappe.model.document import Document
# import re
# from frappe import _


# class DocumentVersion(Document):
#     @frappe.whitelist()
#     def on_submit(self, new_status="Pending"):
#         self.status = new_status
#         self.save()

#     @frappe.whitelist()
#     def approve(self):
#         self.status = "Approved"
#         self.save()

#     @frappe.whitelist()
#     def reject(self):
#         self.status = "Rejected"
#         self.save()
    
     


# wokring good for if document verion approve it also get reflected over document 

# Import required libraries
import frappe
from frappe.model.document import Document

class DocumentVersion(Document):
    @frappe.whitelist()
    def approve(self):
        # Update the Document Version status
        self.status = "Approved"
        self.save()

        # Update the linked Document status
        doc = frappe.get_doc("Document", self.document_name)
        doc.status = "Approved"
        doc.save()
        frappe.db.commit()

    @frappe.whitelist()
    def reject(self):
        # Update the Document Version status
        self.status = "Rejected"
        self.save()

        # Update the linked Document status
        doc = frappe.get_doc("Document", self.document_name)
        doc.status = "Rejected"
        doc.save()
        frappe.db.commit()





# Re-Approval Process

# from frappe.model.document import Document
# import frappe

# class DocumentVersion(Document):
    
#     @frappe.whitelist()    
#     def validate(self):
#         # Reset status to 'Pending' if there are modifications after approval or rejection
#         if self.docstatus == 1 and self.is_dirty():
#             if self.status in ['Approved', 'Rejected']:
#                 self.status = 'Pending'
#                 frappe.msgprint('This document has been modified and requires reapproval.')
    
#     @frappe.whitelist()
#     def approve(self):
#         # Update the Document Version status
#         self.status = "Approved"
#         self.save()

#         # Update the linked Document status
#         doc = frappe.get_doc("Document", self.document_name)
#         doc.status = "Approved"
#         doc.save()
#         frappe.db.commit()

#     @frappe.whitelist()
#     def reject(self):
#         # Update the Document Version status
#         self.status = "Rejected"
#         self.save()

#         # Update the linked Document status
#         doc = frappe.get_doc("Document", self.document_name)
#         doc.status = "Rejected"
#         doc.save()
#         frappe.db.commit()

