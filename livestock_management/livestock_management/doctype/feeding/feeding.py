# Copyright (c) 2026, Henriette and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Feeding(Document):
    def on_submit(self):
        if self.entry_type == "Individual" and self.animal_id:
            livestock = frappe.get_doc("Livestock", self.animal_id)
            livestock.total_feeding_cost = livestock.total_feeding_cost + self.total_cost
            livestock.append("feeding_history", {
                "feeding_id": self.name,
                "feeding_date": self.feeding_date,
                "product": self.product,
                "quantity": self.quantity,
                "total_cost": self.total_cost
            })
            livestock.save()

        elif self.entry_type == "Group" and self.group_id:
            animals = frappe.get_all("Livestock",
                filters={
                    "animal_group": self.group_id,
                    "status": "Active"
                },
                fields=["name"]
            )

            if animals:
                cost_per_animal = self.total_cost / len(animals)

                for animal in animals:
                    livestock = frappe.get_doc("Livestock", animal.name)
                    livestock.total_feeding_cost = livestock.total_feeding_cost + cost_per_animal
                    livestock.append("feeding_history", {
                        "feeding_id": self.name,
                        "feeding_date": self.feeding_date,
                        "product": self.product,
                        "quantity": self.quantity,
                        "total_cost": cost_per_animal
                    })
                    livestock.save()




