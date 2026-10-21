import frappe

from accountsapp.accountsapp.utils import format_price


def get_context(context):
	context.no_cache = 1

	items = frappe.get_all(
		"Item",
		fields=["name", "item_name", "price", "stock_qty", "category", "description"],
		filters={"stock_qty": [">", 0]},
		order_by="category asc, item_name asc",
	)

	for item in items:
		item["price_str"] = format_price(item["price"])

	context.items = items
