# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "trupper"
app_title = "TRUPPER"
app_publisher = "Yefri Tavarez"
app_description = "A Frappe based application for fixing and adding extra functionalities to ERPNext app"
app_icon = "fa fa-free-code-camp"
app_color = "#232315"
app_email = "yefritavarez@tzcode.tech"
app_license = "General Public License, v3"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/trupper/css/trupper.css"
# app_include_js = "/assets/trupper/js/trupper.js"

# include js, css files in header of web template
# web_include_css = "/assets/trupper/css/trupper.css"
# web_include_js = "/assets/trupper/js/trupper.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "trupper.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "trupper.install.before_install"
# after_install = "trupper.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "trupper.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"trupper.tasks.all"
# 	],
# 	"daily": [
# 		"trupper.tasks.daily"
# 	],
# 	"hourly": [
# 		"trupper.tasks.hourly"
# 	],
# 	"weekly": [
# 		"trupper.tasks.weekly"
# 	]
# 	"monthly": [
# 		"trupper.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "trupper.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "trupper.event.get_events"
# }

