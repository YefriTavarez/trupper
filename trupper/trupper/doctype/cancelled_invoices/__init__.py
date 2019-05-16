# -*- coding: utf-8 -*-
# Copyright (c) 2019, Yefri Tavarez and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

def add_to_cancelled_invoices(invoice_type, invoice_name):
	from frappe import new_doc

	# Create a new record
	doc = new_doc("Cancelled Invoices")

	# Update the new record with passed invoice id

	doc.update({
		"invoice_type": invoice_type,
		"invoice_name": invoice_name,
	})

	# Save to the database to persist

	doc.save(ignore_permissions=True)
