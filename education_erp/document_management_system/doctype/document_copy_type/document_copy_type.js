// Copyright (c) 2024, ppcrc and contributors
// For license information, please see license.txt

frappe.ui.form.on("Document Copy Type", {
	refresh(frm) {

        frm.get_field('attachment').df.onchange = function() {
            const file = frm.get_field('attachment').value;
            if (file) {
                const fileFormat = file.split('.').pop();
                frm.set_value('format', fileFormat);
            }
        };

	},
});
