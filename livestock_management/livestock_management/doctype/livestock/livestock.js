// Copyright (c) 2026, Henriette and contributors
// For license information, please see license.txt

frappe.ui.form.on("Livestock", {
	refresh: function(frm) {
        frm.trigger("calculate_closing_valuation");
    },
    opening_valuation_rate: function(frm) {
        frm.trigger("calculate_closing_valuation");
    },
    total_treatment_cost: function(frm) {
        frm.trigger("calculate_closing_value");
    },
    total_feeding_cost: function(frm) {
        frm.trigger("calculate_closing_valuation");
    },
    calculate_closing_valuation: function(frm) {
        var closing = (frm.doc.opening_valuation_rate || 0) +
                      (frm.doc.total_treatment_cost || 0 ) +
                      (frm.doc.total_feeding_cost || 0);
        frm.set_value("closing_valuation_rate", closing);
    }
});


// 	},
// });
