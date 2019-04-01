# -*- coding: utf-8 -*-
# Copyright (c) 2019, Yefri Tavarez and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

from frappe import _
from frappe.utils import flt, cint

class DiscountTermsTemplate(Document):
	def validate(self):
		self.validate_discount_rate()
		self.validate_expire_in_days()
		self.check_duplicate_terms()

	def validate_discount_rate(self):
		for term in self.terms:
			if cint(term.discount_rate) > 0:
				continue

			frappe.throw(_("Invalid Discount Rate: must be greater than zero!"))

	def validate_expire_in_days(self):
		for term in self.terms:
			if cint(term.expire_in_days) > 0:
				continue

			frappe.throw(_("Invalid Expire in Days: must be greater than zero!"))

	def check_duplicate_terms(self):
		terms = []

		msg = _('The Discount Term at row {0} is possibly a duplicate.')

		for term in self.terms:
			term_info = (term.expire_in_days, term.discount_rate)

			if term_info in terms:
				frappe.msgprint(msg.format(term.idx))
			else:
				terms.append(term_info)

