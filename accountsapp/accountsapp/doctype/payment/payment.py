# Copyright (c) 2026, primalkz and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Payment(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		amended_from: DF.Link | None
		amount: DF.Currency
		customer: DF.Link | None
		linked_invoice: DF.Link | None
		mode: DF.Literal["Cash", "Bank", "UPI"]
		payment_date: DF.Date | None
		status: DF.Literal["Draft", "Completed"]
	# end: auto-generated types

	_DOCTYPE_NAME = "Payment"

	def validate(self):
		if not self.amount or self.amount <= 0:
			frappe.throw("Amount must be greater than zero")
		
		if self.linked_invoice:
			total = frappe.db.get_value("Sales Invoice", self.linked_invoice, "total_amount") or 0
			if self.amount > total:
				frappe.throw(f"Payment {self.amount} cannot exceed total amount in linked invoice: {total}")

	def on_submit(self):
		frappe.get_doc({
			"doctype": "Ledger Entry",
			"posting_date": self.payment_date,
			"account": "Cash",
			"party": self.customer,
			"debit": self.amount,
			"credit": 0,
			"voucher_type": self.doctype,
			"voucher_no": self.name,
		}).insert(ignore_permissions=True)

		frappe.get_doc({
			"doctype": "Ledger Entry",
			"posting_date": self.payment_date,
			"account": "Accounts Receivable",
			"party": self.customer,
			"debit": 0,
			"credit": self.amount,
			"voucher_type": self.doctype,
			"voucher_no": self.name,
		}).insert(ignore_permissions=True)

		if self.linked_invoice:
			frappe.db.set_value("Sales Invoice", self.linked_invoice, "status", "Paid")

	def on_cancel(self):
		frappe.db.set_value("Ledger Entry",
		{"voucher_type": self.doctype, "voucher_no": self.name}, "is_cancelled", 1)

		if self.linked_invoice:
			frappe.db.set_value("Sales Invoice", self.linked_invoice, "status", "Submitted")
