import frappe

from accountsapp.accountsapp.utils import format_price


def get_context(context):
	context.no_cache = 1

	context.currency = frappe.db.get_default("currency")
	context.currency_symbol = (
		frappe.db.get_value("Currency", context.currency, "symbol") if context.currency else ""
	)

	items = frappe.get_all(
		"Item",
		fields=["name", "item_name", "price", "category", "stock_qty"],
		filters={"stock_qty": [">", 0]},
		order_by="category asc, item_name asc",
	)

	for item in items:
		item["price_str"] = format_price(item["price"])

	context.items = items

	context.customer = (
		frappe.db.get_value("Customer", {"email": frappe.session.user}, "name")
		if frappe.session.user != "Guest"
		else None
	)
