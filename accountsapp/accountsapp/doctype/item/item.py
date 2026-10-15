# Copyright (c) 2026, primalkz and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class Item(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		category: DF.Data | None
		description: DF.Data | None
		item_code: DF.Data
		item_name: DF.Data
		price: DF.Currency
		stock_qty: DF.Float
	# end: auto-generated types

	_DOCTYPE_NAME = "Item"
