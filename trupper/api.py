# -*- coding: utf-8 -*-
# Copyright (c) 2019, Yefri Tavarez and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe

from frappe.utils import flt, add_days, getdate

@frappe.whitelist()
def get_discount_terms(terms_template, posting_date=None, total=None, bill_date=None):
	if not terms_template:
		return

	terms_doc = frappe.get_doc("Discount Terms Template", terms_template)

	schedule = []
	for d in terms_doc.get("terms"):
		term_details = get_discount_term_details(d, posting_date, total, bill_date)
		schedule.append(term_details)

	return schedule


@frappe.whitelist()
def get_discount_term_details(term, posting_date=None, total=None, bill_date=None):
	term_details = frappe._dict()
	if isinstance(term, basestring):
		term = frappe.get_doc("Discount Term", term)
	else:
		term_details.discount_term = term.discount_term

	discount_amount = flt(term.discount_rate) * flt(total) / 100

	term_details.update({
		"description": term.description,
		"discount_rate": term.discount_rate,
		"discount_amount": discount_amount,
		"expire_in_days": term.expire_in_days,
    })

	if bill_date:
		term_details.due_date = get_due_date(term, bill_date)
	elif posting_date:
		term_details.due_date = get_due_date(term, posting_date)

	if getdate(term_details.due_date) < getdate(posting_date):
		term_details.due_date = posting_date
	# term_details.mode_of_payment = term.mode_of_payment

	return term_details

def get_due_date(term, posting_date=None, bill_date=None):
	due_date = None

	date = bill_date or posting_date

	# if term.due_date_based_on == "Day(s) after invoice date":
	# 	due_date = add_days(date, term.expire_in_days)
	# elif term.due_date_based_on == "Day(s) after the end of the invoice month":
	# 	due_date = add_days(get_last_day(date), term.expire_in_days)
	# elif term.due_date_based_on == "Month(s) after the end of the invoice month":
	# 	due_date = add_months(get_last_day(date), term.credit_months)

	return add_days(date, term.expire_in_days)
