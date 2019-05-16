# -*- coding: utf-8 -*-
# Copyright (c) 2019, Yefri Tavarez and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document


class CancelledInvoices(Document):

    def validate(self):
        from frappe import throw, db, _

        # Check if the document exists in the Database

        if not db.exists(self.invoice_type, self.invoice_name):
            throw(_("Sales Invoice: {} not found")
                  .format(self.invoice_name))

        # Fetch the document docstatus
        docstatus = db.get_value(self.invoice_type, self.invoice_name,
                                 "docstatus")

        # Check the docstatus founds
        if docstatus != 0:
            throw(_("Invalid Sales Invoice docstatus {}")
                  .format(self.invoice_name))
