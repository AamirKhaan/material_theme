frappe.provide("material.theme");

$(document).on("toolbar_setup", function () {
	const root = document.documentElement;
	const theme_mode = root.getAttribute("data-theme-mode");
	if (theme_mode !== "material") {
		return;
	}

	render_clear_demo_action();

	frappe.call({
		method: "material_theme.theme_api.get_user_theme_color",
		callback: function (r) {
			const saved = r.message;
			const themeColor = saved ? saved.hex : localStorage.getItem("ItrostackThemeColor") || "#3C6090";
			applyMaterialTheme(themeColor, null);
		},
	});
});

function render_clear_demo_action() {
	const demo_action = $(
		`<a class="dropdown-item" onclick="return material.theme.clear_demo()">
			${__("Change Theme Color")}
		</a>`
	);
	demo_action.appendTo($("#toolbar-user"));
}

function applyMaterialTheme(SelectedColor, colorName) {
	const hex = SelectedColor.startsWith("#") ? SelectedColor : "#" + SelectedColor;
	const r = document.querySelector(":root");
	const theme = themeFromSourceColor(argbFromHex(hex), [
		{
			name: "custom-1",
			value: argbFromHex(hex),
			blend: true,
		},
	]);

	applyTheme(theme, { target: document.body });

	const color = hexFromArgb(theme.schemes.light.primary);
	localStorage.setItem("ItrostackThemeColor", color);
	r.style.setProperty("--primary", color);

	if (
		colorName &&
		frappe.session.user &&
		frappe.session.user !== "Guest"
	) {
		frappe.call({
			method: "material_theme.theme_api.set_user_theme_color",
			args: { color_name: colorName },
		});
	}
}

material.theme.clear_demo = function () {
	let themeColor = localStorage.getItem("ItrostackThemeColor");
	if (!themeColor) themeColor = "#3C6090";
	if (!themeColor.startsWith("#")) themeColor = "#" + themeColor;

	const inputId = "material-theme-color-input-" + frappe.utils.get_random(8);
	const d = new frappe.ui.Dialog({
		title: __("Select Color"),
		fields: [
			{
				fieldtype: "HTML",
				fieldname: "color_picker",
				options: `
					<div class="form-group">
						<label class="control-label">${__("Custom Color")}</label>
						<input type="color" id="${inputId}" value="${themeColor}" style="width: 100%; height: 48px; border: 1px solid var(--border-color); border-radius: 4px; cursor: pointer; padding: 2px; background: var(--control-bg);">
					</div>
				`,
			},
		],
	});

	d.set_primary_action(__("Set Color"), function () {
		const input = document.getElementById(inputId);
		const customHex = input ? input.value : null;
		if (customHex) {
			applyMaterialTheme(customHex, null);
			d.hide();
			frappe.show_alert({ message: __("Theme color updated"), indicator: "blue" });
		}
	});

	d.show();
};
