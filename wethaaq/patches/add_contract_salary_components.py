import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def execute():
	custom_fields = {
		"Wethaaq Contract": [
			{
				"fieldname": "salary_structure_assignment",
				"label": "Salary Structure Assignment",
				"fieldtype": "Link",
				"options": "Salary Structure Assignment",
				"insert_after": "salary_section",
				"read_only": 1,
			},
			{
				"fieldname": "variables",
				"label": "Incentives / الحوافز",
				"fieldtype": "Currency",
				"options": "currency",
				"insert_after": "basic_salary",
				"read_only": 1,
			},
			{
				"fieldname": "representative_transportation_allowance",
				"label": "Representative Transportation Allowance / بدل انتقال مندوب",
				"fieldtype": "Currency",
				"options": "currency",
				"insert_after": "variables",
				"read_only": 1,
			},
			{
				"fieldname": "other_expenses",
				"label": "Other Expenses / مصروفات أخرى",
				"fieldtype": "Currency",
				"options": "currency",
				"insert_after": "representative_transportation_allowance",
				"read_only": 1,
			},
			{
				"fieldname": "car_rent",
				"label": "Car Rent / إيجار سيارة",
				"fieldtype": "Currency",
				"options": "currency",
				"insert_after": "other_expenses",
				"read_only": 1,
			},
			{
				"fieldname": "safe_allowance",
				"label": "Safe Allowance / بدل خزنة",
				"fieldtype": "Currency",
				"options": "currency",
				"insert_after": "car_rent",
				"read_only": 1,
			},
		],
	}

	create_custom_fields(custom_fields, update=True)
	frappe.clear_cache(doctype="Wethaaq Contract")
