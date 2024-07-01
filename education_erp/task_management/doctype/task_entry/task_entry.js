
frappe.ui.form.on("Task Entry", {
	refresh(frm) {
    frm.set_query('task_sub_category', function(doc) {
        return {
            filters: {
                task_category: doc.task_category
            }
        }
    });


    frm.set_query('task_name', function(doc) {
        return {
            filters: {
                task_subcategory: doc.task_sub_category
            }
        }
    });

	},
});