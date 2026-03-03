import frappe
from frappe import _

def get_context(context):
	name = frappe.form_dict.get("name")
	token = frappe.form_dict.get("token")
	
	if not name or not token:
		context.error_message = _("Invalid link. Missing parameters.")
		return context

	frappe.flags.ignore_permissions = True
	try:
		if not frappe.db.exists("Wethaaq Contract", name):
			context.error_message = _("Contract not found.")
			return context

		contract = frappe.get_doc("Wethaaq Contract", name)

		if not contract.content_hash or contract.content_hash[:10] != token:
			context.error_message = _("Invalid or expired token.")
			return context

		context.contract = contract
		context.has_signature = bool(contract.employee_signature)
		
		# Pre-fetch template HTML
		context.template_html = ""
		if contract.template:
			template_content = frappe.db.get_value("Wethaaq Contract Template", contract.template, "content")
			if template_content:
				context.template_html = frappe.render_template(template_content, {"doc": contract})
				
		# Pre-fetch appendices HTML
		context.appendices_html_list = []
		if contract.appendices:
			for appx in contract.appendices:
				if appx.clause:
					clause_html = appx.clause_content or frappe.db.get_value("Wethaaq Clause", appx.clause, "content")
					if clause_html:
						clause_rendered = frappe.render_template(clause_html, {"doc": contract})
					else:
						clause_rendered = ""
					context.appendices_html_list.append({
						"clause": appx.clause,
						"html": clause_rendered
					})

	finally:
		frappe.flags.ignore_permissions = False

	return context

@frappe.whitelist(allow_guest=True)
def submit_signature(name, token, signature):
	if not name or not token or not signature:
		frappe.throw(_("Missing required parameters"))

	frappe.flags.ignore_permissions = True
	try:
		if not frappe.db.exists("Wethaaq Contract", name):
			frappe.throw(_("Contract not found"))

		contract = frappe.get_doc("Wethaaq Contract", name)
		if not contract.content_hash or contract.content_hash[:10] != token:
			frappe.throw(_("Invalid token"))
			
		if contract.employee_signature:
			frappe.throw(_("Contract is already signed."))

		# Frappe's Signature field can accept the raw Data URI string
		contract.db_set("employee_signature", signature)
		contract.db_set("status", "Signed")
		contract.add_comment("Comment", _("Contract signed successfully by employee."))
	finally:
		frappe.flags.ignore_permissions = False

	return {"status": "success"}
