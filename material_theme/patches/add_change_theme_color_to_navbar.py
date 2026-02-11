import frappe


def execute():
	"""Add Change Theme Color to Navbar Settings when Material theme is installed."""
	navbar_settings = frappe.get_single("Navbar Settings")

	if frappe.db.exists("Navbar Item", {"item_label": "Change Theme Color"}):
		return

	navbar_settings.append(
		"settings_dropdown",
		{
			"item_label": "Change Theme Color",
			"item_type": "Action",
			"action": "material.theme.clear_demo()",
			"is_standard": 1,
			"condition": "document.documentElement.getAttribute('data-theme-mode') === 'material'",
		},
	)

	navbar_settings.save()
