// Copyright (c) 2019, Yefri Tavarez and contributors
// For license information, please see license.txt

frappe.ui.form.on('Discount Terms Template', {
	refresh: frm => {
		frm.add_fetch("discount_term", "description", "description");
	}
});
