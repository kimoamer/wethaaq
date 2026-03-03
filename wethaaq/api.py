import frappe
from frappe import _


@frappe.whitelist()
def get_contract_summary(employee: str) -> dict:
	"""Returns active contracts for a given employee.

	GET /api/method/wethaaq.api.get_contract_summary?employee=HR-EMP-001
	"""
	if not frappe.db.exists("Employee", employee):
		frappe.throw(_("Employee {0} not found").format(employee), frappe.DoesNotExistError)

	contracts = frappe.get_all(
		"Wethaaq Contract",
		filters={"employee": employee, "status": "Active"},
		fields=["name", "contract_type", "start_date", "end_date", "basic_salary", "content_hash"],
		order_by="start_date desc",
	)

	return {
		"status": "success",
		"employee": employee,
		"active_contracts": contracts,
	}


@frappe.whitelist()
def generate_contract_hash(contract_name: str) -> dict:
	"""Manually regenerates the content hash for a contract (audit / integrity check).

	POST /api/method/wethaaq.api.generate_contract_hash
	Body: { "contract_name": "CONT-0001" }
	"""
	# has_permission raises PermissionError automatically if denied
	frappe.has_permission("Wethaaq Contract", ptype="write", doc=contract_name, throw=True)

	doc = frappe.get_doc("Wethaaq Contract", contract_name)
	doc.freeze_contract_version()
	doc.save()  # respects normal permissions — no ignore_permissions bypass

	return {
		"status": "success",
		"contract": contract_name,
		"hash": doc.content_hash,
	}


@frappe.whitelist()
def get_templates_for_type(contract_type: str) -> list:
	"""Returns available templates filtered by contract type.

	Used by client scripts for safe, server-authorised template dropdowns.
	GET /api/method/wethaaq.api.get_templates_for_type?contract_type=Fixed
	"""
	return frappe.get_all(
		"Wethaaq Contract Template",
		filters={"contract_type": contract_type},
		fields=["name", "template_name"],
		order_by="template_name asc",
	)


@frappe.whitelist()
def get_employee_contracts(employee: str, status: str = None) -> dict:
	"""Comprehensive contract list for an employee with optional status filter.

	GET /api/method/wethaaq.api.get_employee_contracts?employee=HR-EMP-001&status=Active
	"""
	if not frappe.db.exists("Employee", employee):
		frappe.throw(_("Employee {0} not found").format(employee), frappe.DoesNotExistError)

	filters = {"employee": employee}
	if status:
		filters["status"] = status

	contracts = frappe.get_all(
		"Wethaaq Contract",
		filters=filters,
		fields=[
			"name", "contract_type", "status",
			"start_date", "end_date", "basic_salary",
			"template", "template_name", "content_hash",
		],
		order_by="start_date desc",
	)

	return {
		"status": "success",
		"employee": employee,
		"contracts": contracts,
		"total": len(contracts),
	}
