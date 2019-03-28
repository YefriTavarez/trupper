# -*- coding: utf-8 -*-
# Copyright (c) 2019, Yefri Tavarez and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

"""Module for handling the jobs of the Scheduler Events"""

__all__ = ["all", "daily", "hourly", "weekly", "monthly"]


def all():
	pass


def daily():
	"""Method that is run every day

		In this method is pretended to do all the required
	tasks in order to update all unpaid invoices.
	"""

	from .utils import get_unpaid_invoices, \
		cancel_unpaid_invoices, \
		ammend_unpaid_invoices, \
		add_record_to_cancelled_invoices, \
		remove_discount_to_unpaid_invoices, \
		submit_unpaid_invoices

	# First things first.
	#
	# Bring all the unpaid invoices to memory
	# This way should be faster as we are going to
	# Read and write only when necessary

	unpaid_invoices = get_unpaid_invoices()

	# All this methods depends on and will work on the
	# Previous list of unpaid and overdue invoices

	# First step is to cancel them

	cancel_unpaid_invoices(unpaid_invoices)

	# Next ammend and leave as Draft.
	# We should return a list of draft invoices
	#
	# Let's catch that and call it as such!

	draft_invoices = ammend_unpaid_invoices(unpaid_invoices)

	# From now on, we should work only with the draft_invoices list
	# Let's do the switch!
	#
	# Add the new invoice to the cancelled invoices list
	# To prevent future cancellations

	add_record_to_cancelled_invoices(draft_invoices)

	# We are ready now to remove the discount from the newly
	# created invoice.

	remove_discount_to_unpaid_invoices(draft_invoices)

	# Finally let's submit the list of draft invoices
	# And continue business as usual

	submit_unpaid_invoices(draft_invoices)


def hourly():
	pass


def weekly():
	pass


def monthly():
	pass
