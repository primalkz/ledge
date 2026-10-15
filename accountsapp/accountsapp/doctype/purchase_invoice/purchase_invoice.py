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
