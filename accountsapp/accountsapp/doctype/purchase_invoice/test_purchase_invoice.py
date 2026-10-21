# Copyright (c) 2026, primalkz and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase

from accountsapp.accountsapp.utils import ensure_chart_of_accounts, get_item, get_supplier

EXTRA_TEST_RECORD_DEPENDENCIES = []
IGNORE_TEST_RECORD_DEPENDENCIES = []


class IntegrationTestPurchaseInvoice(IntegrationTestCase):
	"""Integration tests for Purchase Invoice."""

	def make_invoice(self, rows, supplier="Test Supplier"):
		ensure_chart_of_accounts()
		get_item("T-PUR-1", price=100, stock_qty=10)
		get_supplier(supplier)

		return frappe.get_doc({
			"doctype": "Purchase Invoice",
			"supplier": supplier,
			"invoice_date": "2026-10-19",
			"items": rows,
		}).insert()

	def test_total_is_the_sum_of_the_rows(self):
		invoice = self.make_invoice([
			{"item": "T-PUR-1", "qty": 2, "amount": 200},
			{"item": "T-PUR-1", "qty": 1, "amount": 250},
		])

		self.assertEqual(invoice.total_amount, 450)

	def test_rate_is_worked_out_from_the_amount(self):
		invoice = self.make_invoice([{"item": "T-PUR-1", "qty": 4, "amount": 100}])

		self.assertEqual(invoice.items[0].rate, 25)
		self.assertEqual(invoice.items[0].amount, 100)
		self.assertEqual(invoice.total_amount, 100)

	def test_rate_is_zero_without_a_quantity(self):
		invoice = self.make_invoice([{"item": "T-PUR-1", "qty": 0, "amount": 100}])

		self.assertEqual(invoice.items[0].rate, 0)
		self.assertEqual(invoice.total_amount, 100)

	def test_submit_posts_to_the_ledger(self):
		invoice = self.make_invoice([{"item": "T-PUR-1", "qty": 1, "amount": 100}])
		invoice.submit()

		entries = frappe.get_all(
			"Ledger Entry",
			filters={"voucher_type": "Purchase Invoice", "voucher_no": invoice.name},
			fields=["account", "debit", "credit"],
		)

		self.assertEqual(len(entries), 2)
		by_account = {e.account: e for e in entries}
		self.assertEqual(by_account["Purchases"].debit, 100)
		self.assertEqual(by_account["Accounts Payable"].credit, 100)
		self.assertEqual(by_account["Accounts Payable"].debit, 0)

	def test_cancel_reverses_the_ledger_entries(self):
		invoice = self.make_invoice([{"item": "T-PUR-1", "qty": 1, "amount": 100}])
		invoice.submit()
		invoice.cancel()

		entries = frappe.get_all(
			"Ledger Entry",
			filters={"voucher_type": "Purchase Invoice", "voucher_no": invoice.name},
			fields=["is_cancelled"],
		)

		self.assertEqual(len(entries), 2)
		for e in entries:
			self.assertEqual(e.is_cancelled, 1)

	def test_stock_is_not_touched_by_a_purchase(self):
		get_item("T-PUR-STOCK", price=100, stock_qty=10)
		ensure_chart_of_accounts()
		get_supplier("Stock Supplier")

		invoice = frappe.get_doc({
			"doctype": "Purchase Invoice",
			"supplier": "Stock Supplier",
			"invoice_date": "2026-10-19",
			"items": [{"item": "T-PUR-STOCK", "qty": 5, "amount": 500}],
		}).insert()
		invoice.submit()

		self.assertEqual(frappe.db.get_value("Item", "T-PUR-STOCK", "stock_qty"), 10)
