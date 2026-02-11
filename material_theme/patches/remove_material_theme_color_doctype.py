# Copyright (c) 2026, Itrostack LLP

import frappe


def execute():
	"""Remove Material Theme Color doctype; use standard Color doctype instead."""
	if frappe.db.exists("DocType", "Material Theme Color"):
		frappe.delete_doc("DocType", "Material Theme Color", force=1)
		frappe.db.commit()
