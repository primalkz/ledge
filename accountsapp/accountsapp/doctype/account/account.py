# Copyright (c) 2026, primalkz and contributors
# For license information, please see license.txt

# import frappe
from frappe.utils.nestedset import NestedSet


class Account(NestedSet):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		account_name: DF.Data
		account_type: DF.Literal["Asset", "Liability", "Income", "Expenses", "Equity"]
		balance: DF.Currency
		description: DF.SmallText | None
		is_group: DF.Check
		lft: DF.Int
		old_parent: DF.Link | None
		parent_account: DF.Link | None
		rgt: DF.Int
	# end: auto-generated types

	_DOCTYPE_NAME = "Account"
