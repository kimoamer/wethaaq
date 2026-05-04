# Copyright (c) 2026, Hak3em and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
import hashlib


class WethaaqContract(Document):
	# ── Lifecycle Hooks ────────────────────────────────────────────

	def validate(self):
		self.validate_dates()
		self.validate_active_employee()

	def before_submit(self):
		self.freeze_contract_version()
		if self.status == "Draft":
			self.status = "Review"

	def on_submit(self):
		self.status = "Active"
		self._log_hris_event(f"Contract {self.name} activated for {self.employee}. Basic Salary: {self.basic_salary}")

	def on_cancel(self):
		self.status = "Terminated"
		self._log_hris_event(f"Contract {self.name} cancelled/terminated for {self.employee}.")

	# ── Validations ────────────────────────────────────────────────

	def validate_dates(self):
		if self.end_date and self.start_date and self.end_date < self.start_date:
			frappe.throw(_("End Date cannot be before Start Date"))

	def validate_active_employee(self):
		"""Ensures the linked employee is in Active status, not just that they exist.
		(Frappe already validates Link existence; this adds the status check.)
		"""
		employee_status = frappe.db.get_value("Employee", self.employee, "status")
		if employee_status and employee_status != "Active":
			frappe.throw(_("Employee {0} is not Active (current status: {1})").format(
				self.employee, employee_status
			))

	# ── Contract Integrity ─────────────────────────────────────────

	def freeze_contract_version(self):
		"""Generates a SHA-256 content hash over all material contract fields
		to simulate document integrity tracking (ISO 15489).
		"""
		appendix_ids = "|".join(
			sorted(row.clause for row in self.appendices if row.clause)
		)
		content_str = (
			f"{self.employee}"
			f"|{self.start_date}"
			f"|{self.end_date}"
			f"|{self.basic_salary}"
			f"|{self.template}"
			f"|{self.governing_law or ''}"
			f"|{self.job_offer or ''}"
			f"|{appendix_ids}"
		)
		self.content_hash = hashlib.sha256(content_str.encode("utf-8")).hexdigest()

	# ── E-Signature ────────────────────────────────────────────────

	@frappe.whitelist()
	def send_for_esignature(self):
		"""Dispatches contract securely via email to the employee for signature.
		Updates status to indicate the document is out for signing.
		"""
		allowed_statuses = {"Review", "Draft", "Active"}
		if self.status not in allowed_statuses:
			frappe.throw(
				_("Cannot send for e-signature when contract status is '{0}'").format(self.status)
			)

		if not self.content_hash:
			self.freeze_contract_version()

		employee_email = frappe.db.get_value("Employee", self.employee, "company_email")
		if not employee_email:
			employee_email = frappe.db.get_value("Employee", self.employee, "personal_email")
			
		if not employee_email:
			frappe.throw(_("Employee must have a Company Email or Personal Email set to receive the contract."))

		token = self.content_hash[:10]
		site_url = frappe.utils.get_url()
		sign_url = f"{site_url}/contract_sign?name={self.name}&token={token}"

		# Send the email to the employee
		subject = _("Signature Required: Employment Contract {0}").format(self.name)
		message = f"""
		<p>Dear {self.employee_name or self.employee},</p>
		<p>Your employment contract (<b>{self.name}</b>) is ready for your review and signature.</p>
		<p>Please click the secure link below to review the terms and provide your electronic signature:</p>
		<p><a href="{sign_url}" style="display:inline-block;padding:10px 20px;background:#007bff;color:#fff;text-decoration:none;border-radius:4px;">Review & Sign Contract</a></p>
		<p>If you have any questions, please contact the HR department.</p>
		"""

		frappe.sendmail(
			recipients=[employee_email],
			subject=subject,
			message=message,
			reference_doctype="Wethaaq Contract",
			reference_name=self.name
		)

		self.db_set("evidence_pack_uri", sign_url)
		self.db_set("status", "Signed")

		self._log_hris_event(f"Contract {self.name} sent for e-signature to {employee_email}.")
		return sign_url

	@frappe.whitelist()
	def mark_as_active(self):
		"""Marks a Signed contract as Active"""
		if self.status != "Signed":
			frappe.throw(_("Only Signed contracts can be marked as Active."))
		
		self.db_set("status", "Active")
		self._log_hris_event(f"Contract {self.name} marked as Active manually.")

	@frappe.whitelist()
	def terminate_contract(self, termination_date=None, reason=None):
		"""Terminates an Active or Signed contract"""
		if self.status in ["Terminated", "Cancelled", "Expired"]:
			frappe.throw(_("Contract is already in an inactive state ({0}).").format(self.status))
			
		if not termination_date:
			termination_date = frappe.utils.today()
			
		if frappe.utils.getdate(termination_date) < frappe.utils.getdate(self.start_date):
			frappe.throw(_("Termination date cannot be before the contract start date."))
			
		self.db_set("status", "Terminated")
		self.db_set("termination_date", termination_date)
		if reason:
			self.db_set("termination_reason", reason)
			
		log_msg = f"Contract {self.name} terminated manually on {termination_date}."
		if reason:
			log_msg += f" Reason: {reason}"
		self._log_hris_event(log_msg)

	# ── Internal Helpers ───────────────────────────────────────────

	def _log_hris_event(self, message: str):
		"""Logs an informational HRIS integration event (not an error)."""
		frappe.logger("wethaaq.hris").info(message)





def on_submit_hook(doc, method):
	"""doc_events hook — placeholder for future cross-app on_submit logic."""
	pass


@frappe.whitelist()
def fetch_clauses_from_template(template):
	"""Returns the ordered list of clauses from a Wethaaq Contract Template.
	Called by the contract form when a template is selected.
	"""
	if not template:
		return []

	template_doc = frappe.get_doc("Wethaaq Contract Template", template)
	clauses = []
	for row in template_doc.get("clauses", []):
		clause_content = row.clause_content
		if not clause_content and row.clause:
			clause_content = frappe.db.get_value("Wethaaq Clause", row.clause, "content")
		clauses.append({
			"clause": row.clause,
			"clause_content": clause_content or "",
		})
	return clauses
