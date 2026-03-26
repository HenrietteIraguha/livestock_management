# Copyright (c) 2026, Henriette and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Treatment(Document):
    def on_submit(self):
        if self.entry_type == "Individual" and self.animal_id:
            livestock = frappe.get_doc("Livestock", self.animal_id)
            livestock.total_treatment_cost = livestock.total_treatment_cost + self.total_cost
            livestock.append("treatment_history", {
                "treatment_id": self.name,
                "treatment_date": self.treatment_date,
                "product": self.product,
                "veterinarian": self.veterinarian,
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
                    livestock.total_treatment_cost = livestock.total_treatment_cost + cost_per_animal
                    livestock.append("treatment_history", {
                        "treatment_id": self.name,
                        "treatment_date": self.treatment_date,
                        "product": self.product,
                        "veterinarian": self.veterinarian,
                        "quantity": self.quantity,
                        "total_cost": cost_per_animal
                    })
                    livestock.save()