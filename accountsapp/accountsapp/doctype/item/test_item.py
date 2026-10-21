# Copyright (c) 2026, primalkz and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase

EXTRA_TEST_RECORD_DEPENDENCIES = []
IGNORE_TEST_RECORD_DEPENDENCIES = []


class IntegrationTestItem(IntegrationTestCase):
	"""Integration tests for Item."""

	def test_item_is_created_with_price_and_stock(self):
		item = frappe.get_doc({
			"doctype": "Item",
			"item_code": "T-CASE-1",
			"item_name": "Test Case",
			"price": 249.5,
			"stock_qty": 12,
			"category": "Test",
		}).insert()

		self.assertEqual(item.name, "T-CASE-1")
		self.assertEqual(item.item_name, "Test Case")
		self.assertEqual(item.price, 249.5)
		self.assertEqual(item.stock_qty, 12)

	def test_stock_can_be_written_back(self):
		frappe.get_doc({
			"doctype": "Item",
			"item_code": "T-CASE-2",
			"item_name": "Test Case Two",
			"price": 50,
			"stock_qty": 3,
		}).insert()

		frappe.db.set_value("Item", "T-CASE-2", "stock_qty", 7)

		self.assertEqual(frappe.db.get_value("Item", "T-CASE-2", "stock_qty"), 7)

	def test_item_without_a_price_is_rejected(self):
		with self.assertRaises(frappe.exceptions.MandatoryError):
			frappe.get_doc({
				"doctype": "Item",
				"item_code": "T-CASE-3",
				"item_name": "Test Case Three",
			}).insert()
