frappe.ui.form.on("Sales Invoice", {
	refresh: frm => {
		frm.trigger("run_refresh_methods");
	},
	onload_post_render: frm => {
		// pass
	},
	run_refresh_methods: frm => {
		$.map([
			"toggle_read_only_discounts_fields",
		], event => {
			frm.trigger(event);
		});
	},
	posting_date: frm => {
		frm.trigger("sync_discount_terms_table");
	},
	discount_terms_template: frm => {
		$.map([
			"sync_discount_terms_table",
			"toggle_read_only_discounts_fields",
		], event => {
			frm.trigger(event);
		});
	},
	update_discount_terms_table: frm => {
		frm.trigger("sync_discount_terms_table");
	},
	sync_discount_terms_table: frm => {
		const { doc } = frm,
			posting_date = doc.posting_date
				|| doc.transaction_date;

		if(!doc.discount_terms_template) {
			return false;
		}

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
		});
	},
	update_discount_amounts: frm => {
		const { doc } = frm,
		{ datetime } = frappe,
		{ nowdate } = datetime,
		discount_schedule = doc.discount_schedule,
		{
			discount_amount = .000,
			discount_rate = .000,
		} = discount_schedule.find(d => {
			return d.due_date > nowdate();
		}) || {};

		$.each({
			"apply_discount_on": "Grand Total",
			"additional_discount_percentage": discount_rate,
			"discount_amount":  discount_amount,
		}, (fieldname, value) => {
			frm.set_value(fieldname, value);
		});
	},
	toggle_read_only_discounts_fields: frm => {
		const { doc } = frm;

		$.map([
			"apply_discount_on",
			"additional_discount_percentage",
			"discount_amount",
		], fieldname => {
			frappe.run_serially([
				()=> frappe.timeout(0.5),
				() => frm.toggle_enable(fieldname,
					!doc.discount_terms_template),
			])
		});
	},
});

frappe.ui.form.on("Discount Schedule", {
	discount_term: (frm, cdt, cdn) => {
		const row = frappe.get_doc(cdt, cdn);

		if(!row.discount_term) {
			return false;
		}

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
		});
	},
});
