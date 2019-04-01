// Copyright (c) 2019, Yefri Tavarez and contributors
// For license information, please see license.txt

frappe.ui.form.on('Discount Term', {
	discount_rate: frm => {
		const { doc } = frm;

		if (doc.discount_rate) {
			frm.trigger("update_description");
		}
	},
	expire_in_days: frm => {
		const { doc } = frm;

		if (doc.expire_in_days) {
			frm.trigger("update_description");
		}
	},
	update_description: frm => {
		const { doc } = frm,
		desc = __("{0}% off if invoice is paid within {1} days", [
			doc.discount_rate  || 0,
			doc.expire_in_days || 0,
		]);

		frm.set_value("description", desc);
	},
});
