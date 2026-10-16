# Copyright (c) 2026, primalkz and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class SalesInvoice(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from accountsapp.accountsapp.doctype.sales_invoice_item.sales_invoice_item import SalesInvoiceItem
		from frappe.types import DF

		amended_from: DF.Link | None
		customer: DF.Link | None
		invoice_date: DF.Date | None
		items: DF.Table[SalesInvoiceItem]
		status: DF.Literal["Draft", "Submitted", "Paid"]
		total_amount: DF.Currency
	# end: auto-generated types

	_DOCTYPE_NAME = "Sales Invoice"

	def validate(self):
		for row in self.items:
			row.amount = (row.qty or 0) * (row.rate or 0)
		self.total_amount = sum(row.amount for row in self.items)

	def on_submit(self):
		self.make_ledger_entries()
		self.update_stock()
		self.db_set("status", "Submitted")  # temporarily adding so on website checkout works

	def on_cancel(self):
		self.make_ledger_entries(cancel=True)
		self.update_stock(restore=True)

	def update_stock(self, restore=False):
		sign = 1 if restore else -1
		for row in self.items:
			if not row.item:
				continue
			frappe.db.sql(
				"UPDATE `tabItem` SET stock_qty = stock_qty + %s WHERE name = %s",
				(sign * (row.qty or 0), row.item),
			)

	def make_ledger_entries(self, cancel=False):
		if cancel:
			frappe.db.set_value("Ledger Entry", 
			{
				"voucher_type": self.doctype, "voucher_no": self.name,
			}, "is_cancelled", 1)
			return

		rows = [
			{"account": "Accounts Receivable", "party": self.customer, "debit": self.total_amount, "credit": 0},
			{"account": "Sales", "party": self.customer, "debit": 0, "credit": self.total_amount}
		]

		for r in rows:
			frappe.get_doc({
				"doctype": "Ledger Entry",
				"posting_date": self.invoice_date,
				"voucher_type": self.doctype,
				"voucher_no": self.name,
				**r,
			}).insert(ignore_permissions=True)