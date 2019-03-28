# -*- coding: utf-8 -*-
# Copyright (c) 2019, Yefri Tavarez and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document


class CancelledInvoices(Document):

    def validate(self):
        from frappe import throw, db, _

        # Set doctype to a variable for easier manipulation
        doctype = "Sales Invoice"

        # Check if the document exists in the Database

        if not db.exists(doctype, self.sales_invoice):
            throw(_("Sales Invoice: {} not found")
                  .format(self.sales_invoice))

        # Fetch the document docstatus
        docstatus = db.get_value(doctype, self.sales_invoice,
                                 "docstatus")

        # Check the docstatus founds
        if docstatus != 0:
            throw(_("Invalid Sales Invoice docstatus {}")
                  .format(self.sales_invoice))
