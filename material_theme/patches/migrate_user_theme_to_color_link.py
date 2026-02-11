# Copyright (c) 2026, Itrostack LLP

import frappe


def execute():
	"""Replace material_theme_color_hex (Color) with material_theme_color (Link to Color) on User."""
	# Remove old custom field if exists
	old_cf = frappe.db.exists("Custom Field", {"dt": "User", "fieldname": "material_theme_color_hex"})
	if old_cf:
		frappe.delete_doc("Custom Field", old_cf, force=1)

	# Add new Link to Color custom field
	if frappe.db.exists("Custom Field", {"dt": "User", "fieldname": "material_theme_color"}):
		return
	frappe.get_doc(
		{
			"doctype": "Custom Field",
			"dt": "User",
			"fieldname": "material_theme_color",
			"label": "Material Theme Color",
			"fieldtype": "Link",
			"options": "Color",
			"insert_after": "desk_theme",
			"depends_on": "eval:doc.desk_theme == 'Material'",
			"description": "Your preferred color when using the Material theme.",
			"module": "Material Theme",
		}
	).insert(ignore_permissions=True)
	frappe.db.commit()
