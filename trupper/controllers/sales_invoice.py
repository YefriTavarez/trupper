# -*- coding: utf-8 -*-
# Copyright (c) 2019, Yefri Tavarez and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

from frappe.utils import cstr, nowdate

def validate(doc, method):
	update_discount_amount(doc, method)

def update_discount_amount(doc, method):
	valid_discounts = _get_valid_discounts(doc.discount_schedule)

	amt = max([d.discount_amount for d in valid_discounts] or [.000])

	for fieldname, value in (
		("apply_discount_on", "Grand Total"),
		("discount_amount",  amt),
	):
		if doc.get(fieldname) \
			and not value:
			continue

		doc.set(fieldname, value)

def _get_valid_discounts(base_array):
	_valid_discounts = []

	for d in base_array:
		if cstr(d.due_date) > nowdate():
			_valid_discounts.append(d)

	return _valid_discounts
