# Copyright (c) 2026, primalkz and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase

from accountsapp.accountsapp.utils import ensure_chart_of_accounts, get_customer, get_item

EXTRA_TEST_RECORD_DEPENDENCIES = []
IGNORE_TEST_RECORD_DEPENDENCIES = []


class IntegrationTestSalesInvoice(IntegrationTestCase):
	"""Integration tests for Sales Invoice."""

	def make_invoice(self, rows, customer="Test Customer"):
		ensure_chart_of_accounts()
		get_item("T-INV-1", price=100, stock_qty=10)
		get_customer(customer)

		return frappe.get_doc({
			"doctype": "Sales Invoice",
			"customer": customer,
			"invoice_date": "2026-10-19",
			"items": rows,
		}).insert()

	def test_total_is_the_sum_of_the_rows(self):
		invoice = self.make_invoice([
			{"item": "T-INV-1", "qty": 2, "rate": 100},
			{"item": "T-INV-1", "qty": 3, "rate": 50},
		])

		self.assertEqual(invoice.items[0].amount, 200)
		self.assertEqual(invoice.items[1].amount, 150)
		self.assertEqual(invoice.total_amount, 350)

	def test_submit_posts_to_the_ledger(self):
		invoice = self.make_invoice([{"item": "T-INV-1", "qty": 1, "rate": 100}])
		invoice.submit()

		entries = frappe.get_all(
			"Ledger Entry",
			filters={"voucher_type": "Sales Invoice", "voucher_no": invoice.name},
			fields=["account", "debit", "credit"],
		)

		self.assertEqual(len(entries), 2)
		by_account = {e.account: e for e in entries}
		self.assertEqual(by_account["Accounts Receivable"].debit, 100)
		self.assertEqual(by_account["Accounts Receivable"].credit, 0)
		self.assertEqual(by_account["Sales"].credit, 100)
		self.assertEqual(by_account["Sales"].debit, 0)

	def test_submit_marks_the_invoice_as_submitted(self):
		invoice = self.make_invoice([{"item": "T-INV-1", "qty": 1, "rate": 100}])
		invoice.submit()

		self.assertEqual(invoice.status, "Submitted")
		self.assertEqual(invoice.docstatus, 1)

	def test_submit_reduces_the_stock(self):
		get_item("T-INV-STOCK", price=100, stock_qty=10)
		ensure_chart_of_accounts()
		get_customer("Stock Customer")

		invoice = frappe.get_doc({
			"doctype": "Sales Invoice",
			"customer": "Stock Customer",
			"invoice_date": "2026-10-19",
			"items": [{"item": "T-INV-STOCK", "qty": 4, "rate": 100}],
		}).insert()
		invoice.submit()

		self.assertEqual(frappe.db.get_value("Item", "T-INV-STOCK", "stock_qty"), 6)

	def test_cancel_reverses_the_ledger_and_gives_the_stock_back(self):
		get_item("T-INV-CANCEL", price=100, stock_qty=10)
		ensure_chart_of_accounts()
		get_customer("Cancel Customer")

		invoice = frappe.get_doc({
			"doctype": "Sales Invoice",
			"customer": "Cancel Customer",
			"invoice_date": "2026-10-19",
			"items": [{"item": "T-INV-CANCEL", "qty": 3, "rate": 100}],
		}).insert()
		invoice.submit()
		invoice.cancel()

		entries = frappe.get_all(
			"Ledger Entry",
			filters={"voucher_type": "Sales Invoice", "voucher_no": invoice.name},
			fields=["is_cancelled"],
		)
		self.assertEqual(len(entries), 2)
		for e in entries:
			self.assertEqual(e.is_cancelled, 1)

		self.assertEqual(frappe.db.get_value("Item", "T-INV-CANCEL", "stock_qty"), 10)
