// Copyright (c) 2026, Henriette and contributors
// For license information, please see license.txt

frappe.ui.form.on("Feeding", {
    quantity: function(frm) {
        frm.set_value("total_cost", frm.doc.quantity * frm.doc.valuation_rate);
    },
    valuation_rate: function(frm) {
        frm.set_value("total_cost", frm.doc.quantity * frm.doc.valuation_rate);
    },
    product: function(frm) {
        if (frm.doc.product) {
            frappe.db.get_value("Item", frm.doc.product, "valuation_rate", function(r) {
                if (r) {
                    frm.set_value("valuation_rate", r.valuation_rate);
                }
            });
        }
    }
});
// 	refresh(frm) {

// 	},
// });
