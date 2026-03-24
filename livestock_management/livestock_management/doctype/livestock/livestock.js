// Copyright (c) 2026, Henriette and contributors
// For license information, please see license.txt

frappe.ui.form.on("Livestock", {
	refresh: function(frm) {
        frm.trigger("calculate_closing_valuation");

        frm.set_query("breed",function() {
            return{
                filters: { "animal_type": frm.doc.animal_type}

            };
        });

        frm.set_query("animal_group", function() {
            return {
                filters: {"animal_type": frm.doc.animal_type}
            };
        });
        
    if (frm.doc.status==="Active") {
        frm.add_custom_button('Log Activity', () => {
            let dialog = new frappe.ui.Dialog({
                title: 'Log Activity',
                fields: [
                 { label:'Reason for termination',
                   fieldname:'reason',
                   fieldtype:'Select',
                   options:'Sold\nDead\nMissing\nSlaughtered',
                   reqd:1 
                 },
                 {
                    label: 'Customer',
                    fieldname: 'customer',
                    fieldtype:'Link',
                    options:'Customer',
                    depends_on:'eval:doc.reason=="Sold"',
                    mandatory_depends_on: 'eval:doc.reason=="Sold"'
                 },
                 
                 { label: 'Selling price',
                   fieldname:'selling_price',
                   fieldtype: 'Currency',
                   depends_on: 'eval:doc.reason=="Sold"',
                   mandatory_depends_on: 'eval:doc.reason=="Sold"'

                }

            ],
               primary_action_label: 'Submit',
               primary_action(values) {
                frappe.call({
                    method: 'livestock_management.livestock_management.doctype.livestock.livestock.terminate_livestock',
                    args: {
                        livestock_id: frm.doc.name,
                        reason: values.reason,
                        customer: values.customer || null,
                        selling_price: values.selling_price || null
                    },
                    callback: function(r) {
                        dialog.hide();
                        frm.reload_doc();
                    }
                });
            }
        });
        dialog.show();
    });
    }

     },animal_type: function(frm) {
        frm.set_value("breed", "");
        frm.set_value("animal_group", "")
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
