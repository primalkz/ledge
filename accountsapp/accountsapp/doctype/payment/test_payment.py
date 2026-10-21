# Copyright (c) 2026, primalkz and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase

from accountsapp.accountsapp.utils import ensure_chart_of_accounts, get_customer, get_item

EXTRA_TEST_RECORD_DEPENDENCIES = []
IGNORE_TEST_RECORD_DEPENDENCIES = []


class IntegrationTestPayment(IntegrationTestCase):
	"""Integration tests for Payment."""

	def make_invoice(self, customer="Paying Customer"):
		ensure_chart_of_accounts()
		get_item("T-PAY-1", price=100, stock_qty=10)
		get_customer(customer)

		invoice = frappe.get_doc({
			"doctype": "Sales Invoice",
			"customer": customer,
			"invoice_date": "2026-10-19",
			"items": [{"item": "T-PAY-1", "qty": 1, "rate": 100}],
		}).insert()
		invoice.submit()

		return invoice

	def make_payment(self, amount=100, customer="Paying Customer", linked_invoice=None):
		return frappe.get_doc({
			"doctype": "Payment",
			"payment_date": "2026-10-19",
			"customer": customer,
			"amount": amount,
			"mode": "Cash",
			"linked_invoice": linked_invoice,
		}).insert()

	def test_submit_posts_cash_against_the_receivable(self):
		invoice = self.make_invoice()
		payment = self.make_payment(amount=100, linked_invoice=invoice.name)
		payment.submit()

		entries = frappe.get_all(
			"Ledger Entry",
			filters={"voucher_type": "Payment", "voucher_no": payment.name},
			fields=["account", "debit", "credit"],
		)

		self.assertEqual(len(entries), 2)
		by_account = {e.account: e for e in entries}
		self.assertEqual(by_account["Cash"].debit, 100)
		self.assertEqual(by_account["Accounts Receivable"].credit, 100)

	def test_payment_marks_the_invoice_as_paid(self):
		invoice = self.make_invoice()
		payment = self.make_payment(amount=100, linked_invoice=invoice.name)
		payment.submit()

		self.assertEqual(frappe.db.get_value("Sales Invoice", invoice.name, "status"), "Paid")

	def test_cancel_puts_the_invoice_back_to_submitted(self):
		invoice = self.make_invoice()
		payment = self.make_payment(amount=100, linked_invoice=invoice.name)
		payment.submit()
		payment.cancel()

		self.assertEqual(frappe.db.get_value("Sales Invoice", invoice.name, "status"), "Submitted")

	def test_zero_amount_is_rejected(self):
		self.make_invoice()

		with self.assertRaises(frappe.ValidationError):
			self.make_payment(amount=0)

	def test_payment_larger_than_the_invoice_is_rejected(self):
		invoice = self.make_invoice()

		with self.assertRaises(frappe.ValidationError):
			self.make_payment(amount=500, linked_invoice=invoice.name)
