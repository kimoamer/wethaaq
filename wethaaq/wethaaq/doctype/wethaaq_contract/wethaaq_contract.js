// Copyright (c) 2026, Hak3em and contributors
// For license information, please see license.txt

frappe.ui.form.on("Wethaaq Contract", {

    // ── Form Lifecycle ──────────────────────────────────────────────

    setup(frm) {
        // Filter: only Active employees
        frm.set_query("employee", () => ({
            filters: { status: "Active" }
        }));

        // Filter: only templates matching selected contract type
        frm.set_query("template", () => {
            if (frm.doc.contract_type) {
                return { filters: { contract_type: frm.doc.contract_type } };
            }
        });

        // Filter: departments belonging to the selected company
        frm.set_query("department", () => {
            if (frm.doc.company) {
                return { filters: { company: frm.doc.company } };
            }
        });

        // Query for job offer can be scoped if needed
        frm.set_query("job_offer", () => ({
            filters: { docstatus: 1, status: "Accepted" } // Only show Accepted submitted offers
        }));
    },

    refresh(frm) {
        if (frm.doc.docstatus === 1) {
            if (["Draft", "Review", "Active"].includes(frm.doc.status)) {
                frm.add_custom_button(__("Send for E-Signature"), () => {
                    frappe.confirm(
                        __("Send contract {0} for e-signature?", [frm.doc.name]),
                        () => {
                            frappe.call({
                                method: "send_for_esignature",
                                doc: frm.doc,
                                callback(r) {
                                    if (!r.exc) {
                                        frappe.msgprint(__("Contract sent for E-Signature. Evidence URI tracked."));
                                        frm.reload_doc();
                                    }
                                }
                            });
                        }
                    );
                }, __("Actions"));
            }

            if (frm.doc.status === "Signed") {
                frm.add_custom_button(__("Mark as Active"), () => {
                    frappe.confirm(
                        __("Mark this contract as Active?"),
                        () => {
                            frappe.call({
                                method: "mark_as_active",
                                doc: frm.doc,
                                callback(r) {
                                    if (!r.exc) {
                                        frappe.msgprint(__("Contract marked as Active."));
                                        frm.reload_doc();
                                    }
                                }
                            });
                        }
                    );
                }, __("Actions"));
            }

            if (!["Terminated", "Cancelled", "Expired"].includes(frm.doc.status)) {
                frm.add_custom_button(__("Terminate Contract"), () => {
                    frappe.prompt([
                        {
                            label: __("Termination Date"),
                            fieldname: "termination_date",
                            fieldtype: "Date",
                            reqd: 1,
                            default: frappe.datetime.get_today()
                        },
                        {
                            label: __("Reason for Termination"),
                            fieldname: "reason",
                            fieldtype: "Data",
                            reqd: 1
                        }
                    ], (values) => {
                        frappe.confirm(
                            __("Terminate contract {0}? This cannot be undone.", [frm.doc.name]),
                            () => {
                                frappe.call({
                                    method: "terminate_contract",
                                    doc: frm.doc,
                                    args: {
                                        termination_date: values.termination_date,
                                        reason: values.reason
                                    },
                                    callback(r) {
                                        if (!r.exc) {
                                            frappe.msgprint(__("Contract terminated."));
                                            frm.reload_doc();
                                        }
                                    }
                                });
                            }
                        );
                    }, __("Terminate Contract"), __("Submit"));
                }, __("Actions"));
            }
        }
    },

    // ── Field Events ────────────────────────────────────────────────

    employee(frm) {
        if (!frm.doc.employee) return;

        // Auto-populate company and department from employee record
        frappe.db.get_value("Employee", frm.doc.employee, ["company", "department"], (r) => {
            if (r) {
                frm.set_value("company", r.company || "");
                frm.set_value("department", r.department || "");
            }
        });
    },

    template(frm) {
        if (!frm.doc.template) return;

        frappe.call({
            method: "wethaaq.wethaaq.doctype.wethaaq_contract.wethaaq_contract.fetch_clauses_from_template",
            args: { template: frm.doc.template },
            callback(r) {
                if (!r.message || !r.message.length) return;

                // Clear existing appendices and populate from template
                frm.clear_table("appendices");
                r.message.forEach((clause_row) => {
                    let row = frm.add_child("appendices");
                    row.clause = clause_row.clause;
                    row.clause_content = clause_row.clause_content;
                });
                frm.refresh_field("appendices");
                frappe.show_alert({
                    message: __("{0} clause(s) fetched from template", [r.message.length]),
                    indicator: "green"
                });
            }
        });
    },

    contract_type(frm) {
        // Clear template when type changes to prevent type mismatch
        frm.set_value("template", "");
    },

    company(frm) {
        // Clear department if company changes (avoid cross-company mismatch)
        frm.set_value("department", "");
    },

    job_offer(frm) {
        if (!frm.doc.job_offer) return;
        frappe.db.get_doc("Job Offer", frm.doc.job_offer).then(doc => {
            if (doc.designation) frm.set_value("designation", doc.designation);
            if (doc.company) frm.set_value("company", doc.company);
        });
    },

    basic_salary(frm) {
        frm.trigger("calculate_hourly_rate");
    },
    
    working_hours_per_day(frm) {
        frm.trigger("calculate_hourly_rate");
    },
    
    working_days_per_week(frm) {
        frm.trigger("calculate_hourly_rate");
    },
    
    work_nature(frm) {
        frm.trigger("calculate_hourly_rate");
    },

    calculate_hourly_rate(frm) {
        if (frm.doc.basic_salary && frm.doc.working_hours_per_day && frm.doc.working_days_per_week) {
            let weekly_hours = frm.doc.working_hours_per_day * frm.doc.working_days_per_week;
            let hourly_rate = 0;
            
            // "Daily / يومى", "Weekly / أسبوعى", "Monthly / شهرى"
            if (frm.doc.work_nature && frm.doc.work_nature.includes("Daily")) {
                hourly_rate = frm.doc.basic_salary / frm.doc.working_hours_per_day;
            } else if (frm.doc.work_nature && frm.doc.work_nature.includes("Weekly")) {
                hourly_rate = frm.doc.basic_salary / weekly_hours;
            } else { 
                // Monthly default
                hourly_rate = (frm.doc.basic_salary * 12) / (52 * weekly_hours);
            }
            frm.set_value("hourly_rate", flt(hourly_rate, 2));
        }
    }
});
