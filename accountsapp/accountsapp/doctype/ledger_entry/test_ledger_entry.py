# Copyright (c) 2026, primalkz and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase

from accountsapp.accountsapp.utils import ensure_chart_of_accounts

EXTRA_TEST_RECORD_DEPENDENCIES = []
IGNORE_TEST_RECORD_DEPENDENCIES = []


class IntegrationTestLedgerEntry(IntegrationTestCase):
	"""Integration tests for Ledger Entry."""

	def make_entry(self, account="Cash", debit=0, credit=0, voucher_no="TEST-1"):
		return frappe.get_doc({
			"doctype": "Ledger Entry",
			"posting_date": "2026-10-19",
			"account": account,
			"debit": debit,
			"credit": credit,
			"voucher_type": "Journal Entry",
			"voucher_no": voucher_no,
		}).insert()

	def test_entry_keeps_the_amount_it_was_posted_with(self):
		ensure_chart_of_accounts()

		entry = self.make_entry(debit=500)

		self.assertEqual(entry.debit, 500)
		self.assertEqual(entry.credit, 0)
		self.assertEqual(entry.account, "Cash")
		self.assertEqual(frappe.db.get_value("Ledger Entry", entry.name, "debit"), 500)

	def test_entry_is_not_cancelled_when_it_is_created(self):
		ensure_chart_of_accounts()

		entry = self.make_entry(credit=125)

		self.assertEqual(entry.is_cancelled, 0)

	def test_entries_can_be_marked_cancelled(self):
		ensure_chart_of_accounts()

		entry = self.make_entry(debit=75)
		frappe.db.set_value("Ledger Entry", entry.name, "is_cancelled", 1)

		self.assertEqual(frappe.db.get_value("Ledger Entry", entry.name, "is_cancelled"), 1)

	def test_debit_and_credit_can_both_be_left_empty(self):
		ensure_chart_of_accounts()

		entry = self.make_entry()

		self.assertEqual(entry.debit, 0)
		self.assertEqual(entry.credit, 0)
