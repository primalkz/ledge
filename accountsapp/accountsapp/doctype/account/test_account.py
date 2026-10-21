# Copyright (c) 2026, primalkz and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase

from accountsapp.accountsapp.utils import ensure_chart_of_accounts

EXTRA_TEST_RECORD_DEPENDENCIES = []
IGNORE_TEST_RECORD_DEPENDENCIES = []


class IntegrationTestAccount(IntegrationTestCase):
	"""Integration tests for Account."""

	def test_account_is_created_under_its_parent(self):
		ensure_chart_of_accounts()

		account = frappe.get_doc({
			"doctype": "Account",
			"account_name": "Test Bank",
			"account_type": "Asset",
			"parent_account": "Assets",
		}).insert()

		self.assertEqual(account.name, "Test Bank")
		self.assertEqual(account.parent_account, "Assets")
		self.assertEqual(frappe.db.get_value("Account", "Test Bank", "account_type"), "Asset")

	def test_group_account_can_be_created_without_a_parent(self):
		account = frappe.get_doc({
			"doctype": "Account",
			"account_name": "Test Group",
			"account_type": "Asset",
			"is_group": 1,
		}).insert()

		self.assertEqual(account.is_group, 1)
		self.assertIsNone(account.parent_account)

	def test_chart_of_accounts_is_not_created_twice(self):
		ensure_chart_of_accounts()
		before = frappe.db.count("Account")

		ensure_chart_of_accounts()

		self.assertEqual(frappe.db.count("Account"), before)
		self.assertTrue(frappe.db.exists("Account", "Accounts Receivable"))
		self.assertTrue(frappe.db.exists("Account", "Accounts Payable"))
		self.assertTrue(frappe.db.exists("Account", "Cash"))
		self.assertTrue(frappe.db.exists("Account", "Sales"))
		self.assertTrue(frappe.db.exists("Account", "Purchases"))
