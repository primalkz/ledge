# Copyright (c) 2026, primalkz and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters: dict | None = None):
	"""Return columns and data for the report.

	This is the main entry point for the report. It accepts the filters as a
	dictionary and should return columns and data. It is called by the framework
	every time the report is refreshed or a filter is updated.
	"""
	columns = get_columns()
	data = get_data()

	return columns, data

def execute_snapshot_report(filters: dict | None = None):
	"""Return columns and data for the report.

	This is the main entry point for snapshot report. When 'Synced
	Report' is enabled in report, framework will call this method
	every time the report is refreshed or a filter is updated. It
	accepts the same filters as normal execute. But a utility method -
	get_latest_sync, is also imported.

	"""
	from frappe.database.duckdb.database import get_latest_sync

	columns = get_columns()
	data = get_data()

	return columns, data

def get_columns() -> list[dict]:
	return [
		{
			"label": _("Account"),
			"fieldname": "account",
			"fieldtype": "Link",
			"options": "Account",
			"width": 200,
		},
		{
			"label": _("Type"),
			"fieldname": "account_type",
			"fieldtype": "Data",
			"width": 80,
		},
		{
			"label": _("Group"),
			"fieldname": "is_group",
			"fieldtype": "Check",
			"width": 80,
		},
		{
			"label": _("Debit"),
			"fieldname": "debit",
			"fieldtype": "Currency",
			"width": 200,
		},
		{
			"label": _("Credit"),
			"fieldname": "credit",
			"fieldtype": "Currency",
			"width": 200,
		},
		{
			"label": _("Balance"),
			"fieldname": "balance",
			"fieldtype": "Currency",
			"width": 200,
		},
	]


def get_data() -> list[list]:
	"""Return data for the report.

	The report data is a list of rows, with each row being a list of cell values.
	"""
	accounts = frappe.get_all("Account", fields=["name", "account_type", "is_group"], order_by="lft")

	totals = frappe.db.sql("""
	SELECT account, SUM(debit) AS debit, SUM(credit) AS credit FROM `tabLedger Entry` 
	WHERE is_cancelled = 0 GROUP BY account""", as_dict=True)

	totals = {t.account: t for t in totals}

	rows = []
	for acc in accounts:
		t = totals.get(acc.name)
		debit = t.debit if t else 0
		credit = t.credit if t else 0

		if acc.account_type in ("Asset", "Expenses"):
			balance = debit - credit
		else:
			balance = credit - debit

		rows.append({
			"account": acc.name,
			"account_type": acc.account_type,
			"is_group": acc.is_group,
			"debit": debit,
			"credit": credit,
			"balance": balance,
		})
	return rows