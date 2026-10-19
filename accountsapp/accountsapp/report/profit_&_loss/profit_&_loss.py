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
	"""Return columns for the report.

	One field definition per column, just like a DocType field definition.
	"""
	return [
		{
			"label": _("Account"),
			"fieldname": "account",
			"fieldtype": "Data",
			"width": 200,
		},
		{
			"label": _("Account Type"),
			"fieldname": "account_type",
			"fieldtype": "Data",
			"width": 150,
		},
		{
			"label": _("Amount"),
			"fieldname": "amount",
			"fieldtype": "Currency",
			"width": 150,
		},
	]


def get_data() -> list[list]:
	"""Return data for the report.

	The report data is a list of rows, with each row being a list of cell values.
	"""
	accounts = frappe.get_all("Account", fields=["name", "account_type"],
	filters={"is_group": 0, "account_type": ["in", ["Income", "Expenses"]]}, order_by="lft")

	totals = frappe.db.sql("""
	SELECT account, SUM(debit) AS debit, SUM(credit) AS credit FROM `tabLedger Entry` 
	WHERE is_cancelled = 0 GROUP BY account""", as_dict=True)

	totals = {t.account: t for t in totals}

	rows = []
	income = 0
	expenses = 0

	for acc in accounts:
		t = totals.get(acc.name)
		debit = t.debit if t else 0
		credit = t.credit if t else 0
		amount = (credit - debit) if acc.account_type == "Income" else (debit - credit)

		if acc.account_type == "Income":
			income += amount
		else:
			expenses += amount

		rows.append({
			"account": acc.name,
			"account_type": acc.account_type,
			"amount": amount,
		})

	rows.append({"account": "Total Income", "amount": income})
	rows.append({"account": "Total Expenses", "amount": expenses})
	rows.append({"account": "Net Profit/Loss", "amount": income - expenses})
	return rows
