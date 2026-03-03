import frappe
from frappe.utils import add_days, today


def check_contract_expiry():
	"""Daily scheduled job: creates ToDo tracking records for HR staff
	when contracts are expiring soon.

	Email notifications are handled natively by Frappe's Notification engine
	(Wethaaq Contract Expiry fixture). This task only creates system ToDos
	to ensure in-app visibility alongside the email alert.
	"""
	if not frappe.db.exists("Notification", "Wethaaq Contract Expiry"):
		return

	notification = frappe.get_doc("Notification", "Wethaaq Contract Expiry")

	if not notification.enabled:
		return

	days_in_advance = notification.days_in_advance or 30
	target_date = add_days(today(), days_in_advance)

	expiring_contracts = frappe.get_all(
		"Wethaaq Contract",
		filters={"status": "Active", "end_date": target_date},
		fields=["name", "employee", "end_date"],
	)

	if not expiring_contracts:
		return

	# Resolve HR recipient users from notification configuration
	hr_roles = [
		row.receiver_by_role
		for row in notification.recipients
		if row.receiver_by_role
	] or ["HR Manager"]

	hr_users = frappe.get_all(
		"Has Role",
		filters={"role": ["in", hr_roles]},
		fields=["parent"],
	)
	recipient_users = list({u.parent for u in hr_users})

	_create_expiry_todos(expiring_contracts, recipient_users, days_in_advance)

	frappe.db.commit()


def _create_expiry_todos(contracts, recipient_users, days_in_advance):
	"""Creates a ToDo for each (contract, recipient) pair, skipping duplicates."""
	for contract in contracts:
		employee_name = frappe.db.get_value(
			"Employee", contract.employee, "employee_name"
		)
		description = (
			f"Expiring Contract ({days_in_advance} Days): "
			f"{contract.name} for {employee_name}"
		)

		for user in recipient_users:
			_create_todo_if_not_exists(contract.name, user, description)


def _create_todo_if_not_exists(contract_name: str, user: str, description: str):
	"""Inserts a ToDo only if one does not already exist for this contract + user.

	Prevents duplicate ToDos when the scheduler runs on consecutive days.
	"""
	already_exists = frappe.db.exists(
		"ToDo",
		{
			"reference_type": "Wethaaq Contract",
			"reference_name": contract_name,
			"status": "Open",
			"allocated_to": user,
		},
	)

	if already_exists:
		return

	frappe.get_doc(
		{
			"doctype": "ToDo",
			"allocated_to": user,
			"reference_type": "Wethaaq Contract",
			"reference_name": contract_name,
			"description": description,
			"status": "Open",
		}
	).insert(ignore_permissions=True)
