# Copyright (c) 2026, primalkz and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase

from accountsapp.accountsapp.utils import ensure_chart_of_accounts

EXTRA_TEST_RECORD_DEPENDENCIES = []
IGNORE_TEST_RECORD_DEPENDENCIES = []


class IntegrationTestJournalEntry(IntegrationTestCase):
	"""Integration tests for Journal Entry."""

	def make_entry(self, rows):
		ensure_chart_of_accounts()

		return frappe.get_doc({
			"doctype": "Journal Entry",
			"entry_date": "2026-10-19",
			"accounts": rows,
		}).insert()

	def test_totals_are_the_sum_of_the_rows(self):
		entry = self.make_entry([
			{"account": "Cash", "debit": 250, "credit": 0},
			{"account": "Sales", "debit": 0, "credit": 250},
		])

		self.assertEqual(entry.total_debit, 250)
		self.assertEqual(entry.total_credit, 250)

	def test_submit_writes_one_ledger_entry_per_row(self):
		entry = self.make_entry([
			{"account": "Cash", "debit": 250, "credit": 0},
			{"account": "Sales", "debit": 0, "credit": 250},
		])
		entry.submit()

		entries = frappe.get_all(
			"Ledger Entry",
			filters={"voucher_type": "Journal Entry", "voucher_no": entry.name},
			fields=["account", "debit", "credit"],
		)

		self.assertEqual(len(entries), 2)
		by_account = {e.account: e for e in entries}
		self.assertEqual(by_account["Cash"].debit, 250)
		self.assertEqual(by_account["Sales"].credit, 250)

	def test_unbalanced_entry_is_rejected(self):
		with self.assertRaises(frappe.ValidationError):
			self.make_entry([
				{"account": "Cash", "debit": 100, "credit": 0},
				{"account": "Sales", "debit": 0, "credit": 40},
			])

	def test_entry_with_no_amounts_is_rejected(self):
		with self.assertRaises(frappe.ValidationError):
			self.make_entry([
				{"account": "Cash", "debit": 0, "credit": 0},
			])

	def test_cancel_marks_the_ledger_entries_as_cancelled(self):
		entry = self.make_entry([
			{"account": "Cash", "debit": 100, "credit": 0},
			{"account": "Sales", "debit": 0, "credit": 100},
		])
		entry.submit()
		entry.cancel()

		entries = frappe.get_all(
			"Ledger Entry",
			filters={"voucher_type": "Journal Entry", "voucher_no": entry.name},
			fields=["is_cancelled"],
		)

		self.assertEqual(len(entries), 2)
		for e in entries:
			self.assertEqual(e.is_cancelled, 1)
