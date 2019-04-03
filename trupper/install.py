# -*- coding: utf-8 -*-
# Copyright (c) 2019, Yefri Tavarez and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

__all__ = ["before_install", "after_install"]

standard_records = {
	"Discount Term": [
		{
			"description": "2% off if invoice is paid within 90 days",
			"discount_rate": 2.0,
			"discount_term_name": "90 days discount",
			"expire_in_days": 90,
		},
		{
			"description": "5% off if invoice is paid within 60 days",
			"discount_rate": 5.0,
			"discount_term_name": "60 days discount",
			"expire_in_days": 60,
		},
		{
			"description": "10% off if invoice is paid within 30 days",
			"discount_rate": 10.0,
			"discount_term_name": "30 days discount",
			"expire_in_days": 30,
		},
	],
	"Discount Terms Template": [
		{
			"template_name": "Standard Discount",
			"terms": [
				{
					"description": "10% off if invoice is paid within 30 days",
					"discount_rate": 10.0,
					"discount_term": "30 days discount",
					"expire_in_days": 30,
					"parent": "Standard Discount",
					"parentfield": "terms",
					"parenttype": "Discount Terms Template"
				},
				{
					"description": "5% off if invoice is paid within 60 days",
					"discount_rate": 5.0,
					"discount_term": "60 days discount",
					"expire_in_days": 60,
					"parent": "Standard Discount",
					"parentfield": "terms",
					"parenttype": "Discount Terms Template"
				},
				{
					"description": "2% off if invoice is paid within 90 days",
					"discount_rate": 2.0,
					"discount_term": "90 days discount",
					"expire_in_days": 90,
					"parent": "Standard Discount",
					"parentfield": "terms",
					"parenttype": "Discount Terms Template"
				}
			]
		},
	],
}

def before_install():
	pass

def after_install():
	_add_standard_discount_terms()
	_add_standard_discount_terms_template()

def _add_standard_discount_terms():
	from frappe import db

	# set doctype at the top
	doctype = "Discount Term"

	# iterate each record
	for term in standard_records \
		.get(doctype):

		# check the database to see if it exists
		exists = db.exists(doctype, {
			"discount_term_name": term.get("discount_term_name"),
		})

		# if the records exists let's skip it
		# to prevent an error
		if exists:
			continue

		# create an empty doc
		doc = frappe.new_doc(doctype)

		# update with the JSON record
		doc.update(term)

		# save to the Database
		doc.insert()


def _add_standard_discount_terms_template():
	from frappe import db

	# set doctype at the top
	doctype = "Discount Terms Template"

	# iterate each record
	for term in standard_records \
		.get(doctype):

		# check the database to see if it exists
		exists = db.exists(doctype, {
			"template_name": term.get("template_name"),
		})

		# if the records exists let's skip it
		# to prevent an error
		if exists:
			continue

		# create an empty doc
		doc = frappe.new_doc(doctype)

		# update with the JSON record
		doc.update(term)

		# save to the Database
		doc.insert()
