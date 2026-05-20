app_name = "wethaaq"
app_title = "Wethaaq"
app_publisher = "Hak3em"
app_description = "HRIS Contract Management System"
app_email = "a.amer@innomate-tech.com"
app_license = "mit"
app_version = "0.1.0"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "wethaaq",
# 		"logo": "/assets/wethaaq/logo.png",
# 		"title": "Wethaaq",
# 		"route": "/wethaaq",
# 		"has_permission": "wethaaq.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/wethaaq/css/wethaaq.css"
# app_include_js = "/assets/wethaaq/js/wethaaq.js"

# include js, css files in header of web template
# web_include_css = "/assets/wethaaq/css/wethaaq.css"
# web_include_js = "/assets/wethaaq/js/wethaaq.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "wethaaq/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
app_include_icons = "wethaaq/icons/wethaaq/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "wethaaq.utils.jinja_methods",
# 	"filters": "wethaaq.utils.jinja_filters"
# }

# Fixtures — export with: bench export-fixtures
# ----------
# Ensures Notification and Workspace records are bundled with the app
# and auto-imported on: bench migrate / bench install-app
fixtures = [
	{"dt": "Notification", "filters": [["module", "=", "Wethaaq"]]},
	{"dt": "Workspace", "filters": [["module", "=", "Wethaaq"]]},
	{
		"dt": "Custom Field",
		"filters": [
			["name", "in", [
				"Company-custom_legal_representative",
				"Company-custom_legal_representative_title",
				"Company-custom_representatives",
				"Employee-custom_national_id",
				"Employee-custom_governorate",
			]]
		]
	},
]

# Installation
# ------------

# before_install = "wethaaq.install.before_install"
# after_install = "wethaaq.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "wethaaq.uninstall.before_uninstall"
# after_uninstall = "wethaaq.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "wethaaq.utils.before_app_install"
# after_app_install = "wethaaq.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "wethaaq.utils.before_app_uninstall"
# after_app_uninstall = "wethaaq.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "wethaaq.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Wethaaq Contract": {
		"on_submit": "wethaaq.wethaaq.doctype.wethaaq_contract.wethaaq_contract.on_submit_hook",
	}
}

# Scheduled Tasks
# ---------------

scheduler_events = {
	"daily": [
		"wethaaq.tasks.check_contract_expiry"
	]
}

# Testing
# -------

# before_tests = "wethaaq.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "wethaaq.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
override_doctype_dashboards = {
	"Employee": "wethaaq.overrides.dashboard_overrides.get_dashboard_for_employee",
	"Job Offer": "wethaaq.overrides.dashboard_overrides.get_dashboard_for_job_offer"
}

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["wethaaq.utils.before_request"]
# after_request = ["wethaaq.utils.after_request"]

# Job Events
# ----------
# before_job = ["wethaaq.utils.before_job"]
# after_job = ["wethaaq.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"wethaaq.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

