# Copyright (c) 2026, primalkz and contributors

import frappe

# name, account_type, is_group, parent_account
CHART_OF_ACCOUNTS = (
	("Assets", "Asset", 1, None),
	("Cash", "Asset", 0, "Assets"),
	("Accounts Receivable", "Asset", 0, "Assets"),
	("Liabilities", "Liability", 1, None),
	("Accounts Payable", "Liability", 0, "Liabilities"),
	("Income", "Income", 1, None),
	("Sales", "Income", 0, "Income"),
	("Expenses", "Expenses", 1, None),
	("Purchases", "Expenses", 0, "Expenses"),
)


def ensure_chart_of_accounts():
	"""Create the accounts the vouchers post to, unless they are already there."""
	for name, account_type, is_group, parent in CHART_OF_ACCOUNTS:
		if frappe.db.exists("Account", name):
			continue

		frappe.get_doc({
			"doctype": "Account",
			"account_name": name,
			"account_type": account_type,
			"is_group": is_group,
			"parent_account": parent,
		}).insert(ignore_permissions=True)


def get_item(item_code, price=100, stock_qty=10):
	if frappe.db.exists("Item", item_code):
		return frappe.get_doc("Item", item_code)

	return frappe.get_doc({
		"doctype": "Item",
		"item_code": item_code,
		"item_name": item_code,
		"price": price,
		"stock_qty": stock_qty,
	}).insert()


def get_customer(customer_name, email=None):
	if frappe.db.exists("Customer", customer_name):
		return frappe.get_doc("Customer", customer_name)

	return frappe.get_doc({
		"doctype": "Customer",
		"customer_name": customer_name,
		"email": email or f"{customer_name.lower().replace(' ', '.')}@example.com",
	}).insert()


def get_supplier(supplier_name, email=None):
	if frappe.db.exists("Supplier", supplier_name):
		return frappe.get_doc("Supplier", supplier_name)

	return frappe.get_doc({
		"doctype": "Supplier",
		"supplier_name": supplier_name,
		"email": email or f"{supplier_name.lower().replace(' ', '.')}@example.com",
	}).insert()
