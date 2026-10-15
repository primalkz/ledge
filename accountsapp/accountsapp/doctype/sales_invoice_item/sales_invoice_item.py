# Copyright (c) 2026, primalkz and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class SalesInvoiceItem(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		amount: DF.Currency
		item: DF.Link | None
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		qty: DF.Float
		rate: DF.Currency
	# end: auto-generated types

	_DOCTYPE_NAME = "Sales Invoice Item"