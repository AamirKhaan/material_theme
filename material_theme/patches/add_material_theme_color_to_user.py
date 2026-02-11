# Copyright (c) 2026, Itrostack LLP

import frappe


def execute():
	"""Add Material Theme Color field to User doctype for per-user color selection."""
	if frappe.db.exists("Custom Field", {"dt": "User", "fieldname": "material_theme_color_hex"}):
		return
	frappe.get_doc(
		{
			"doctype": "Custom Field",
			"dt": "User",
			"fieldname": "material_theme_color_hex",
			"label": "Material Theme Color",
			"fieldtype": "Color",
			"insert_after": "desk_theme",
			"depends_on": "eval:doc.desk_theme == 'Material'",
			"description": "Your preferred color when using the Material theme.",
			"module": "Material Theme",
		}
	).insert(ignore_permissions=True)
	frappe.db.commit()
