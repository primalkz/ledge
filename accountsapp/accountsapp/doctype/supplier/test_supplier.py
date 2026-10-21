# Copyright (c) 2026, primalkz and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase

EXTRA_TEST_RECORD_DEPENDENCIES = []
IGNORE_TEST_RECORD_DEPENDENCIES = []


class IntegrationTestSupplier(IntegrationTestCase):
	"""Integration tests for Supplier."""

	def test_supplier_is_created_with_an_email(self):
		supplier = frappe.get_doc({
			"doctype": "Supplier",
			"supplier_name": "Test Supplier",
			"email": "test.supplier@example.com",
			"phone": "9000000001",
		}).insert()

		self.assertEqual(supplier.name, "Test Supplier")
		self.assertEqual(supplier.email, "test.supplier@example.com")
		self.assertEqual(frappe.db.get_value("Supplier", "Test Supplier", "phone"), "9000000001")

	def test_supplier_can_be_found_by_email(self):
		frappe.get_doc({
			"doctype": "Supplier",
			"supplier_name": "Second Supplier",
			"email": "second.supplier@example.com",
		}).insert()

		found = frappe.db.get_value("Supplier", {"email": "second.supplier@example.com"}, "name")

		self.assertEqual(found, "Second Supplier")
