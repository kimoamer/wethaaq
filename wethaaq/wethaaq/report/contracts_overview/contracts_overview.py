# Copyright (c) 2026, Hak3em and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	return [
		{
			"fieldname": "contract",
			"label": _("Contract"),
			"fieldtype": "Link",
			"options": "Wethaaq Contract",
			"width": 150
		},
		{
			"fieldname": "employee",
			"label": _("Employee"),
			"fieldtype": "Link",
			"options": "Employee",
			"width": 150
		},
		{
			"fieldname": "employee_name",
			"label": _("Employee Name"),
			"fieldtype": "Data",
			"width": 140
		},
		{
			"fieldname": "department",
			"label": _("Department"),
			"fieldtype": "Link",
			"options": "Department",
			"width": 140
		},
		{
			"fieldname": "status",
			"label": _("Status"),
			"fieldtype": "Data",
			"width": 100
		},
		{
			"fieldname": "contract_type",
			"label": _("Type"),
			"fieldtype": "Data",
			"width": 100
		},
		{
			"fieldname": "template_name",
			"label": _("Template"),
			"fieldtype": "Data",
			"width": 150
		},
		{
			"fieldname": "start_date",
			"label": _("Start Date"),
			"fieldtype": "Date",
			"width": 100
		},
		{
			"fieldname": "end_date",
			"label": _("End Date"),
			"fieldtype": "Date",
			"width": 100
		},
		{
			"fieldname": "basic_salary",
			"label": _("Basic Salary"),
			"fieldtype": "Currency",
			"options": "currency",
			"width": 120
		},
		{
			"fieldname": "currency",
			"label": _("Currency"),
			"fieldtype": "Link",
			"options": "Currency",
			"width": 80
		}
	]


def get_data(filters):
	conditions, values = get_conditions(filters)

	# Row-level permission check from Wethaaq Contract controller will be automatically
	# applied by frappe.db.get_list if we use it, but since this is SQL we need to
	# inject the match conditions if needed. Using get_all is safer for permissions.

	data = frappe.get_all(
		"Wethaaq Contract",
		filters=conditions,
		fields=[
			"name as contract",
			"employee",
			"employee_name",
			"department",
			"status",
			"contract_type",
			"template_name",
			"start_date",
			"end_date",
			"basic_salary",
			"currency"
		],
		order_by="start_date desc"
	)
	
	return data


def get_conditions(filters):
	conditions = {}
	values = {}

	if not filters:
		return conditions, values

	for field in ["company", "department", "status", "contract_type"]:
		if filters.get(field):
			conditions[field] = filters.get(field)

	return conditions, values
