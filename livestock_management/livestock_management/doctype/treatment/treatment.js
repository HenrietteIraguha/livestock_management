// Copyright (c) 2026, Henriette and contributors
// For license information, please see license.txt

frappe.ui.form.on("Treatment", {
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
    },
    entry_type: function(frm) {
        frm.trigger("toggle_fields");
    },
    toggle_fields: function(frm) {
        var is_individual = frm.doc.entry_type === "Individual";
        var is_group = frm.doc.entry_type === "Group";

        frm.toggle_display("animal_id", is_individual);
        frm.toggle_display("group_id", is_group);

        frm.toggle_reqd("animal_id", is_individual);
        frm.toggle_reqd("group_id", is_group);

        if (is_individual) {
            frm.set_value("group_id", "");
        }
        if (is_group) {
            frm.set_value("animal_id", "");
        }
    }
});

// 	refresh(frm) {
// 	},
// });
