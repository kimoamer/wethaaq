// Copyright (c) 2026, Hak3em and contributors
// For license information, please see license.txt

frappe.ui.form.on("Wethaaq Contract Template", {
	refresh(frm) {
		if (frm.doc.clauses && frm.doc.clauses.length) {
			frm.add_custom_button(__("Preview Clauses"), () => {
				let html = "";
				frm.doc.clauses.forEach((row, i) => {
					let title = row.clause_name || row.clause || `Clause ${i + 1}`;
					let content = row.clause_content || "<em>No content</em>";
					html += `<div style="margin-bottom:16px;">
						<h5 style="border-bottom:1px solid #d1d8dd;padding-bottom:4px;">${i + 1}. ${title}</h5>
						<div>${content}</div>
					</div>`;
				});
				frappe.msgprint({
					title: __("Template Clauses Preview"),
					message: html,
					wide: true
				});
			});
		}
	}
});
