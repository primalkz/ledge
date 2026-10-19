import frappe


def get_context(context):
	context.items = frappe.get_all(
		"Item",
		fields=["name", "item_name", "price", "category", "stock_qty"],
		filters={"stock_qty": [">", 0]},
		order_by="category asc, item_name asc",
	)

	context.customer = (
		frappe.db.get_value("Customer", {"email": frappe.session.user}, "name")
		if frappe.session.user != "Guest"
		else None
	)
