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
