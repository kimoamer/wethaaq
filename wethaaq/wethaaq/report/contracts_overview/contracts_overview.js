// Copyright (c) 2026, Hak3em and contributors
// For license information, please see license.txt

frappe.query_reports["Contracts Overview"] = {
	"filters": [
		{
			"fieldname": "company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company")
		},
		{
			"fieldname": "department",
			"label": __("Department"),
			"fieldtype": "Link",
			"options": "Department"
		},
		{
			"fieldname": "status",
			"label": __("Status"),
			"fieldtype": "Select",
			"options": "\nDraft\nReview\nSigned\nActive\nExpired\nTerminated",
			"default": "Active"
		},
		{
			"fieldname": "contract_type",
			"label": __("Contract Type"),
			"fieldtype": "Select",
			"options": "\nFixed\nOpen\nIntern\nFreelance"
		}
	]
};
