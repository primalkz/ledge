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
