# Copyright (c) 2026, primalkz and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class JournalEntry(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from accountsapp.accountsapp.doctype.journal_entry_account.journal_entry_account import JournalEntryAccount
		from frappe.types import DF

		accounts: DF.Table[JournalEntryAccount]
		amended_from: DF.Link | None
		entry_date: DF.Date | None
		title: DF.Data | None
		total_credit: DF.Currency
		total_debit: DF.Currency
	# end: auto-generated types

	_DOCTYPE_NAME = "Journal Entry"

	def validate(self):
		self.total_debit = sum(row.debit or 0 for row in self.accounts)
		self.total_credit = sum(row.credit or 0 for row in self.accounts)
		
		if self.total_debit != self.total_credit:
			frappe.throw(f"Total debit ({self.total_debit}) must be equal to total credit.")

		if not self.total_debit and not self.total_credit:
			frappe.throw("Total debit and total credit have to be non zero.")

	def on_submit(self):
		for r in self.accounts:
			frappe.get_doc({
				"doctype": "Ledger Entry",
				"account": r.account,
				"posting_date": self.entry_date,
				"party": "",
				"debit": r.debit,
				"credit": r.credit,
				"voucher_type": self.doctype,
				"voucher_no": self.name,
			}).insert(ignore_permissions=True)
	
	def on_cancel(self):
		frappe.db.set_value("Ledger Entry", 
		{"voucher_type": self.doctype, "voucher_no": self.name}, "is_cancelled", 1)