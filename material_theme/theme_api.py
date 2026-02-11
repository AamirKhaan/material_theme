# Copyright (c) 2026, Itrostack LLP

import frappe


@frappe.whitelist()
def get_theme_colors():
	"""Return empty list (preset colors removed). Kept for backward compatibility with cached clients."""
	return []


@frappe.whitelist()
def get_user_theme_color():
	"""Return the current user's saved Material theme color: {hex, color_name} or None."""
	user = frappe.session.user
	if user and user != "Guest":
		color_link = frappe.db.get_value("User", user, "material_theme_color")
		if color_link:
			hex_value = frappe.db.get_value("Color", color_link, "color")
			if hex_value:
				hex_val = hex_value if hex_value.startswith("#") else "#" + hex_value
				return {"hex": hex_val, "color_name": color_link}
	return None


@frappe.whitelist()
def set_user_theme_color(color_name=None):
	"""Save the current user's Material theme color preference from Color doctype dropdown selection."""
	user = frappe.session.user
	if not user or user == "Guest":
		frappe.throw(frappe._("You must be logged in to save theme color."))
	# Clear selection when empty
	if not color_name or not str(color_name).strip():
		frappe.db.set_value("User", user, "material_theme_color", None)
		frappe.db.commit()
		return None
	color_name = str(color_name).strip()
	if not frappe.db.exists("Color", color_name):
		frappe.throw(frappe._("Color '{0}' does not exist.").format(color_name))
	frappe.db.set_value("User", user, "material_theme_color", color_name)
	frappe.db.commit()
	hex_value = frappe.db.get_value("Color", color_name, "color")
	return hex_value if hex_value and hex_value.startswith("#") else "#" + (hex_value or "")
