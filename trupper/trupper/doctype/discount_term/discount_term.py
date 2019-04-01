# -*- coding: utf-8 -*-
# Copyright (c) 2019, Yefri Tavarez and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

from frappe import _

class DiscountTerm(Document):
	def validate(self):
		self.validate_discount_rate()
		self.validate_expire_in_days()


	def validate_discount_rate(self):
		if self.discount_rate > 0:
			return

		frappe.throw(_("Invalid Discount Rate: must be greater than zero!"))


	def validate_expire_in_days(self):
		if self.expire_in_days > 0:
			return

		frappe.throw(_("Invalid Expire in Days: must be greater than zero!"))
