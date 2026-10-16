# Copyright (c) 2026, primalkz and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class PurchaseInvoice(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from accountsapp.accountsapp.doctype.purchase_invoice_item.purchase_invoice_item import PurchaseInvoiceItem
		from frappe.types import DF

		amended_from: DF.Link | None
		invoice_date: DF.Date | None
		items: DF.Table[PurchaseInvoiceItem]
		status: DF.Literal["Draft", "Submitted", "Paid"]
		supplier: DF.Link | None
		total_amount: DF.Currency
	# end: auto-generated types

	_DOCTYPE_NAME = "Purchase Invoice"

	def validate(self):
		for row in self.items:
			row.amount = (row.qty or 0) * (row.rate or 0)
		self.total_amount = sum(row.amount for row in self.items)

	def on_submit(self):
		self.make_ledger_entries();

	def on_cancel(self):
		self.make_ledger_entries(cancel=True)

	def make_ledger_entries(self, cancel=False):
		if cancel:
			frappe.db.set_value("Ledger Entry",
			{
				"voucher_type": self.doctype, "voucher_no": self.name,
			}, "is_cancelled", 1)
			return
		
		rows = [
			{"account": "Purchases", "party": self.supplier, "debit": self.total_amount, "credit": 0},
			{"account": "Accounts Payable", "party": self.supplier, "debit": 0, "credit": self.total_amount}
		]

		for r in rows:
			frappe.get_doc({
				"doctype": "Ledger Entry",
				"posting_date": self.invoice_date,
				"voucher_type": self.doctype,
				"voucher_no": self.name,
				**r,
			}).insert(ignore_permissions=True)