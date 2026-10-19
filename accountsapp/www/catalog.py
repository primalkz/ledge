import frappe


def get_context(context):
	context.items = frappe.get_all(
		"Item",
		fields=["name", "item_name", "price", "stock_qty", "category", "description"],
		filters={"stock_qty": [">", 0]},
		order_by="category asc, item_name asc",
	)
