from frappe import _


def get_dashboard_for_employee(data):
	"""Injects Wethaaq Contract link into the Employee dashboard.

	Appends to the existing 'Lifecycle' section if present,
	otherwise creates a new 'Compliance & Contracts' section.
	"""
	lifecycle_section = next(
		(s for s in data.get("transactions", [])
		 if s.get("label") in ["Lifecycle", _("Lifecycle")]),
		None,
	)

	if lifecycle_section:
		lifecycle_section["items"].append("Wethaaq Contract")
	else:
		data["transactions"].append({
			"label": _("Compliance & Contracts"),
			"items": ["Wethaaq Contract"],
		})

	return data


def get_dashboard_for_job_offer(data):
	"""Injects Wethaaq Contract link into the Job Offer dashboard.

	Appends to 'Lifecycle' or 'Reference' if present,
	otherwise creates a new 'Compliance & Contracts' section.
	"""
	target_labels = {"Lifecycle", _("Lifecycle"), "Reference", _("Reference")}

	linked_section = next(
		(s for s in data.get("transactions", [])
		 if s.get("label") in target_labels),
		None,
	)

	if linked_section:
		linked_section["items"].append("Wethaaq Contract")
	else:
		data["transactions"].append({
			"label": _("Compliance & Contracts"),
			"items": ["Wethaaq Contract"],
		})

	return data
