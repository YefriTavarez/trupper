frappe.ui.form.on("Sales Invoice", {
	posting_date: frm => {
		frm.trigger("discount_terms_template");
	},
	discount_terms_template: frm => {
		const { doc } = frm;

		if(doc.discount_terms_template) {
			const posting_date = doc.posting_date || doc.transaction_date;
			frappe.call({
				method: "trupper.api.get_discount_terms",
				args: {
					terms_template: doc.discount_terms_template,
					posting_date: posting_date,
					total: doc.total,
					bill_date: doc.bill_date
				},
				callback: function(response) {
					if (response.message) {
						frm.set_value("discount_schedule", response.message);
					}

					frm.trigger("update_discount_amounts");
				}
			})
		}
	},
	update_discount_amounts: frm => {
		const { doc } = frm,
			{ datetime } = frappe,
			{ nowdate } = datetime;

		const discounts = $.grep(doc.discount_schedule, d => {
			return d.due_date > nowdate();
		}).map(d => {
			return d.discount_amount;
		});

		const amt = Math.max(...discounts);

		$.each({
			"apply_discount_on": "Grand Total",
			"discount_amount":  (Infinity == Math.abs(-amt) ? .000 : amt),
		}, (fieldname, value) => {
			frm.set_value(fieldname, value);
		});
	},
});

frappe.ui.form.on("Discount Schedule", {
	discount_term: (frm, cdt, cdn) => {
		const row = frappe.get_doc(cdt, cdn);

		if(row.discount_term) {
			frappe.call({
				method: "trupper.api.get_discount_term_details",
				args: {
					term: row.discount_term,
					bill_date: frm.doc.bill_date,
					posting_date: frm.doc.posting_date || frm.doc.transaction_date,
					total: frm.doc.total
				},
				callback: function(response) {
					if(response.message) {
						$.each(response.message, (fieldname, value) => {
							frappe.model.set_value(cdt, cdn, d, response.message[d]);
						});
					}
				}
			})
		}
	},
});
