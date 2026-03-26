# Copyright (c) 2026, Henriette and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Livestock(Document):
    def after_insert(self):
        if self.animal_group:
            group = frappe.get_doc("Animal Group", self.animal_group)
            group.total_animals = group.total_animals + 1
            group.save()

        settings = frappe.get_doc("Livestock Account Settings")
        debit_account = settings.debit_account
        credit_account = settings.credit_account

        if debit_account and credit_account and self.opening_valuation_rate:
            je = frappe.get_doc({
                "doctype": "Journal Entry",
                "posting_date": self.date_of_acquire,
                "accounts": [
                    {
                        "account": debit_account,
                        "debit_in_account_currency": self.opening_valuation_rate
                    },
                    {
                        "account": credit_account,
                        "credit_in_account_currency": self.opening_valuation_rate
                    }
                ]
            })
            je.insert()
            je.submit()


@frappe.whitelist()
def terminate_livestock(livestock_id, reason, customer=None, selling_price=None):
    livestock = frappe.get_doc("Livestock", livestock_id)
    livestock.status = reason
    livestock.save()

    frappe.msgprint(f"Status changed to {reason}")

    if livestock.animal_group:
        group = frappe.get_doc("Animal Group", livestock.animal_group)
        group.total_animals = group.total_animals - 1
        group.save()
    
    audit = frappe.get_doc({
        "doctype": "Livestock Record Audit",
        "livestock_id": livestock_id,
        "activity": reason,
        "date_of_action": frappe.utils.now(),
        "valuation_rate": livestock.closing_valuation_rate
    })
    audit.insert()
    audit.submit()

    settings = frappe.get_doc("Livestock Account Settings")

    if settings.debit_account and settings.credit_account and livestock.closing_valuation_rate:
        je = frappe.get_doc({
            "doctype": "Journal Entry",
            "posting_date": frappe.utils.today(),
            "accounts": [
                {
                    "account": settings.credit_account,
                    "debit_in_account_currency": livestock.closing_valuation_rate
                },
                {
                    "account": settings.debit_account,
                    "credit_in_account_currency": livestock.closing_valuation_rate
                }
            ]
        })
        je.insert()
        je.submit()

    if reason == "Sold" and customer:
        if not frappe.db.exists("Item", livestock_id):
            item = frappe.get_doc({
                "doctype": "Item",
                "item_code": livestock_id,
                "item_name": livestock.animal_name or livestock_id,
                "item_group":"Livestock Sales",
                "is_stock_item": 0
            })
            item.insert()

        si = frappe.get_doc({
            "doctype": "Sales Invoice",
            "customer": customer,
            "posting_date": frappe.utils.today(),
            "items": [
                {
                    "item_code": livestock_id,
                    "qty": 1,
                    "rate": livestock.closing_valuation_rate
                }
            ]
        })
        si.insert()
        si.submit()


			