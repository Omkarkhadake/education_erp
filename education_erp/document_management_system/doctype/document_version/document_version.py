# Copyright (c) 2024, ppcrc and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import re
from frappe import _


class DocumentVersion(Document):
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
    
     


