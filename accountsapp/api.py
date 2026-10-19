import frappe
from frappe import _


@frappe.whitelist()
def create_order(cart: str):
	if frappe.session.user == "Guest":
		frappe.throw(_("You must be logged in to create an order."), frappe.PermissionError)

	cart = frappe.parse_json(cart) if isinstance(cart, str) else cart
	if not cart:
		frappe.throw(_("Cart is empty."), frappe.ValidationError)

	customer = frappe.db.get_value("Customer", {"email": frappe.session.user}, "name")
	if not customer:
		frappe.throw(
			_("No customer found for the user {0}.").format(frappe.session.user), frappe.ValidationError
		)

	items = []
	for line in cart:
		item_code = line.get("item")
		qty = float(line.get("qty") or 0)
		if not item_code or qty <= 0:
			continue

		item = frappe.db.get_value("Item", item_code, ["price", "stock_qty"], as_dict=True)

		if not item:
			frappe.throw(_("Item {0} not found.").format(item_code), frappe.ValidationError)

		if qty > (item.stock_qty or 0):
			frappe.throw(
				_("Not enough stock for item {0}. Available: {1}, Requested: {2}").format(
					item_code, item.stock_qty, qty
				),
				frappe.ValidationError,
			)

		items.append({"item": item_code, "qty": qty, "rate": item.price, "amount": item.price * qty})

	if not items:
		frappe.throw(_("Cart is empty."), frappe.ValidationError)

	invoice = frappe.get_doc(
		{
			"doctype": "Sales Invoice",
			"customer": customer,
			"invoice_date": frappe.utils.nowdate(),
			"items": items,
		}
	).insert(ignore_permissions=True)
	invoice.submit()
	return invoice.name
