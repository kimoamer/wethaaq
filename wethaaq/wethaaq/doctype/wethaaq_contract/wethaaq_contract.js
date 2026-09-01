// Copyright (c) 2026, Hak3em and contributors
// For license information, please see license.txt

frappe.ui.form.on("Wethaaq Contract", {

    // ── Form Lifecycle ──────────────────────────────────────────────

    setup(frm) {
        frm.set_query("employee", () => ({
            filters: { status: "Active" }
        }));

        frm.set_query("template", () => {
            if (frm.doc.contract_type) {
                return { filters: { contract_type: frm.doc.contract_type } };
            }
        });

        frm.set_query("department", () => {
            if (frm.doc.company) {
                return { filters: { company: frm.doc.company } };
            }
        });

        frm.set_query("job_offer", () => ({
            filters: { docstatus: 1, status: "Accepted" }
        }));
    },

    refresh(frm) {
        frm.trigger("setup_representatives_options");

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

        frappe.db.get_value("Employee", frm.doc.employee, [
            "employee_name", "company", "department", "custom_national_id",
            "passport_number", "custom_governorate", "current_address"
        ], (r) => {
            if (r) {
                frm.set_value("employee_name", r.employee_name || "");
                frm.set_value("company", r.company || "");
                frm.set_value("department", r.department || "");
                frm.set_value("national_id", r.custom_national_id || "");
                frm.set_value("passport_number", r.passport_number || "");
                frm.set_value("governorate", r.custom_governorate || "");
                frm.set_value("current_address", r.current_address || "");
                frm.trigger("fetch_salary_assignment");
            }
        });
    },

    start_date(frm) {
        frm.trigger("fetch_salary_assignment");
    },

    template(frm) {
        if (!frm.doc.template) return;

        frappe.db.get_value("Wethaaq Contract Template", frm.doc.template, "template_name", (r) => {
            if (r) {
                frm.set_value("template_name", r.template_name || "");
            }
        });

        frappe.call({
            method: "wethaaq.wethaaq.doctype.wethaaq_contract.wethaaq_contract.fetch_clauses_from_template",
            args: { template: frm.doc.template },
            callback(r) {
                if (!r.message || !r.message.length) return;

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
        frm.set_value("template", "");
    },

    company(frm) {
        frm.set_value("department", "");
        frm.set_value("company_representative", "");
        frm.set_value("legal_representative", "");
        frm.set_value("legal_representative_title", "");
        frm.trigger("setup_representatives_options");
        frm.trigger("fetch_salary_assignment");
    },

    company_representative(frm) {
        if (!frm.doc.company_representative) {
            frm.set_value("legal_representative", "");
            frm.set_value("legal_representative_title", "");
            return;
        }

        if (!frm.doc.company) return;

        frappe.db.get_doc("Company", frm.doc.company).then(company_doc => {
            let representatives = company_doc.custom_representatives || [];
            let selected = representatives.find(r => r.representative_name === frm.doc.company_representative);
            if (selected) {
                frm.set_value("legal_representative", selected.representative_name || "");
                frm.set_value("legal_representative_title", selected.title || "");
            }
        });
    },

    setup_representatives_options(frm) {
        if (!frm.doc.company) {
            frm.set_df_property("company_representative", "options", [""]);
            return;
        }

        frappe.db.get_doc("Company", frm.doc.company).then(company_doc => {
            let representatives = company_doc.custom_representatives || [];
            let options = [""];
            representatives.forEach(rep => {
                if (rep.representative_name) {
                    let label = rep.representative_name;
                    if (rep.title) {
                        label += ` (${rep.title})`;
                    }
                    if (rep.branch) {
                        label += ` - ${rep.branch}`;
                    }
                    options.push({
                        value: rep.representative_name,
                        label: label
                    });
                }
            });

            frm.set_df_property("company_representative", "options", options);

            if (!frm.doc.company_representative) {
                let default_rep = representatives.find(r => r.is_default);
                if (default_rep) {
                    frm.set_value("company_representative", default_rep.representative_name);
                }
            }
        });
    },

    fetch_salary_assignment(frm) {
        if (!frm.doc.employee || frm.doc.docstatus !== 0) return;

        frappe.call({
            method: "wethaaq.wethaaq.doctype.wethaaq_contract.wethaaq_contract.get_salary_assignment_details",
            args: {
                employee: frm.doc.employee,
                reference_date: frm.doc.start_date || frappe.datetime.get_today(),
                company: frm.doc.company || null
            },
            callback(r) {
                const values = r.message || {};
                if (!values.salary_structure_assignment) return;

                const fieldnames = [
                    "salary_structure_assignment",
                    "basic_salary",
                    "variables",
                    "representative_transportation_allowance",
                    "other_expenses",
                    "car_rent",
                    "safe_allowance",
                    "currency"
                ];

                fieldnames.forEach((fieldname) => {
                    if (Object.prototype.hasOwnProperty.call(values, fieldname)) {
                        frm.set_value(fieldname, values[fieldname] || 0);
                    }
                });

                frm.trigger("calculate_hourly_rate");
                frappe.show_alert({
                    message: __("Salary values fetched from {0}", [values.salary_structure_assignment]),
                    indicator: "green"
                });
            }
        });
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

            if (frm.doc.work_nature && frm.doc.work_nature.includes("Daily")) {
                hourly_rate = frm.doc.basic_salary / frm.doc.working_hours_per_day;
            } else if (frm.doc.work_nature && frm.doc.work_nature.includes("Weekly")) {
                hourly_rate = frm.doc.basic_salary / weekly_hours;
            } else {
                hourly_rate = (frm.doc.basic_salary * 12) / (52 * weekly_hours);
            }
            frm.set_value("hourly_rate", flt(hourly_rate, 2));
        }
    }
});
