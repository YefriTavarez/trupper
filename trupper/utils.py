# -*- coding: utf-8 -*-
# Copyright (c) 2019, Yefri Tavarez and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

__all__ = [
	"get_unpaid_invoices",
	"cancel_unpaid_invoices",
	"ammend_unpaid_invoices",
	"add_record_to_cancelled_invoices",
	"remove_discount_to_unpaid_invoices",
	"submit_unpaid_invoices",
]


def get_unpaid_invoices():
	"""Search the overdue invoices

	This method fetches all the Overdue invoices from the Database.

	Returns:
		list: A list of Overdue invoices
	"""

	from frappe import get_all, \
			get_doc

	from frappe.utils import today

	# Main doctype that we are going to be working with

	doctype = "Sales Invoice"

	# Let's do the fetch from the Database of all the IDs

	unpaid_invoices = get_all(doctype, {
		"docstatus": ("=", "1"),
		"outstanding_amount": (">", .000),
		"due_date": ("<", today()),
	}, as_list=True)

	# Please don't change from a list to a tuple
	cancelled_invoices = [d.name for d in get_all("Cancelled Invoices")]

	# return a list of docs instead of a list of data

	for docname, in unpaid_invoices:

		doc = get_doc(doctype, docname)

		# If the invoice does not have any discount, we should not cancel it
		# nor edit it.
		#
		# To achieve this: We add the docname of the unpaid invoice
		# To the cancelled_invoices list to prevent from
		# Cancelling as it does not have any discount
		#
		# If the discount is less than or equal to zero and
		# All of its children have discount less than or equal to zero
		# We should definitely tell the system to skip it.

		if not doc.discount_amount > .000 \
			and _has_not_any_discount(doc.items):

			# Tell the system to skip it
			cancelled_invoices.append(docname)

	return [
		get_doc(doctype, docname)
		for docname, in unpaid_invoices
		if docname not in cancelled_invoices
	]


def cancel_unpaid_invoices(unpaid_invoices):
	for doc in unpaid_invoices:
		if doc.docstatus != 1:
			continue

		doc.cancel()


def ammend_unpaid_invoices(unpaid_invoices):
	from frappe import copy_doc

	draft_invoices = []
	for doc in unpaid_invoices:
		if doc.docstatus != 2:
			continue

		# Make a copy of the cancelled document

		amended_doc = copy_doc(doc)

		# Set docstatus to "Draft" to prevent validation
		# Errors when saving

		amended_doc.docstatus = 0

		# Let's link the two docs. The cancelled one
		# and the newly created

		amended_doc.amended_from = doc.name

		# Update all children's docstatus to match with
		# the parent's

		amended_doc.set_docstatus()

		# Tell Frappe that this is a new document

		amended_doc.__islocal = True

		# Finally save to Database

		amended_doc.insert(ignore_permissions=True)

		# The sentence above should left the document in "Draft"
		# Let's add it to the draft_invoices list to return it later

		draft_invoices.append(amended_doc)

	return draft_invoices

def add_record_to_cancelled_invoices(draft_invoices):
	from . import add_to_cancelled_invoices

	for doc in draft_invoices:
		add_to_cancelled_invoices(doc.name)


def remove_discount_to_unpaid_invoices(draft_invoices):
	from frappe import _
	from frappe.utils import flt

	for doc in draft_invoices:

		# The only mode where the user is permitted to
		# Modify or update a Frappe document is when the document
		# Is in Draft.
		#
		# So, if it's different, let's skip the document!

		if doc.docstatus != 0:
			continue

		# Clear additional discount given in the
		# Document

		doc.additional_discount_percentage = \
			doc.discount_amount = \
			doc.base_discount_amount = .000

		for d in doc.items:
			# Discount formula

			# 200 - 200 * (10 / 100) = 180
			#
			# x = 200
			# i = 10
			# s = 180
			#
			# x - x * (i / 100) = s
			#
			# x (1 - (i / 100)) = s
			# x = s / (1 - (i / 100))
			# x = 180 / (1 - (10 / 100.00))
			#
			# Update Rate back to its aprox. Original amount

			if flt(d.price_list_rate):
				d.rate = flt(d.price_list_rate)
			else:
				d.rate = d.rate / (1 - (d.discount_percentage / 100))

			# For each row let's clear the
			# Discount_percentage

			d.discount_percentage = .000

		# Leave a comment

		doc.add_comment("Update", _("Cleared discounts"))

		# Save to the Database the latest changes

		doc.save(ignore_permissions=True)


def submit_unpaid_invoices(draft_invoices):
	for doc in draft_invoices:
		if doc.docstatus != 0:
			continue

		doc.submit()

def _has_not_any_discount(items):
	from frappe.utils import flt

	does_not_has = False

	for d in items:
		if flt(d.discount_percentage) <= .000:
			does_not_has = True

	# Does not have any unless otherwise is proven
	return does_not_has
