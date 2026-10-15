# Copyright (c) 2026, primalkz and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class LedgerEntry(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		account: DF.Link | None
		credit: DF.Currency
		debit: DF.Currency
		is_cancelled: DF.Check
		party: DF.Data | None
		posting_date: DF.Date | None
		voucher_no: DF.Data | None
		voucher_type: DF.Literal["Sales Invoice", "Purchase Invoice", "Journal Entry", "Payment"]
	# end: auto-generated types

	_DOCTYPE_NAME = "Ledger Entry"
