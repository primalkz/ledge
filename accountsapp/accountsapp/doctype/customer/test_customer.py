# Copyright (c) 2026, primalkz and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase

EXTRA_TEST_RECORD_DEPENDENCIES = []
IGNORE_TEST_RECORD_DEPENDENCIES = []


class IntegrationTestCustomer(IntegrationTestCase):
	"""Integration tests for Customer."""

	def test_customer_is_created_with_an_email(self):
		customer = frappe.get_doc({
			"doctype": "Customer",
			"customer_name": "Test Customer",
			"email": "test.customer@example.com",
			"phone": "9000000000",
		}).insert()

		self.assertEqual(customer.name, "Test Customer")
		self.assertEqual(customer.email, "test.customer@example.com")
		self.assertEqual(frappe.db.get_value("Customer", "Test Customer", "phone"), "9000000000")

	def test_customer_can_be_found_by_email(self):
		frappe.get_doc({
			"doctype": "Customer",
			"customer_name": "Second Customer",
			"email": "second.customer@example.com",
		}).insert()

		found = frappe.db.get_value("Customer", {"email": "second.customer@example.com"}, "name")

		self.assertEqual(found, "Second Customer")

	def test_duplicate_customer_name_is_rejected(self):
		frappe.get_doc({
			"doctype": "Customer",
			"customer_name": "Duplicate Name",
			"email": "one@example.com",
		}).insert()

		with self.assertRaises(frappe.DuplicateEntryError):
			frappe.get_doc({
				"doctype": "Customer",
				"customer_name": "Duplicate Name",
				"email": "two@example.com",
			}).insert()
