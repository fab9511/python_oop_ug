import unittest
from unittest.mock import Mock
from InvoiceRepository import InvoiceRepository
from Shop import Shop
from Invoice import Invoice
from Warehouse import Warehouse, OutOfStore


class ShopTests(unittest.TestCase):
    def setUp(self):
        self.mock_repo = Mock(spec=InvoiceRepository)
        self.mock_warehouse = Mock(spec=Warehouse)
        self.shop = Shop(self.mock_repo, self.mock_warehouse)
        self.sample_invoice = Invoice(number=1, customer="Jan", items=[("cukierki", 2), ("chleb", 1)])

    def test_while_buy_the_repository_add_should_be_called(self):
        self.shop.buy(customer="Jan", items_list=[("cukierki", 2)])
        self.mock_repo.add.assert_called_once()

    def test_while_returning_goods_the_repository_returns_false_when_not_find(self):
        self.mock_repo.find_by_number.return_value = None
        result = self.shop.returning_goods(self.sample_invoice)
        self.assertEqual(result, False)

    def test_while_returning_goods_the_repository_delete_should_be_called_when_find(self):
        self.mock_repo.find_by_number.return_value = self.sample_invoice
        self.shop.returning_goods(self.sample_invoice)

        # Sprawdzenie czy metoda delete została wywołana
        self.mock_repo.delete.assert_called_once_with(self.sample_invoice)

    # Testy dla metody buy()
    def test_buy_calls_repository_add(self):
        self.mock_repo.get_next_number.return_value = 1
        self.shop.buy(customer="Jan", items_list=[("cukierki", 2)])
        self.mock_repo.add.assert_called_once()

    def test_buy_calls_warehouse_remove_for_each_item(self):
        items = [("cukierki", 2), ("chleb", 1)]
        self.shop.buy(customer="Jan", items_list=items)

        self.assertEqual(self.mock_warehouse.remove_product.call_count, len(items))

        calls = self.mock_warehouse.remove_product.call_args_list
        for i, (product, quantity) in enumerate(items):
            args, _ = calls[i]
            self.assertEqual(args[0], product)
            self.assertEqual(args[1], quantity)

    def test_buy_returns_correct_invoice(self):
        self.mock_repo.get_next_number.return_value = 123
        items = [("cukierki", 2), ("chleb", 1)]
        invoice = self.shop.buy(customer="Jan", items_list=items)

        self.assertEqual(invoice.number, 123)
        self.assertEqual(invoice.customer, "Jan")
        self.assertEqual(invoice.items, items)

    def test_buy_propagates_warehouse_exception(self):
        self.mock_warehouse.remove_product.side_effect = OutOfStore("Brak produktu")
        with self.assertRaises(OutOfStore):
            self.shop.buy(customer="Jan", items_list=[("cukierki", 2)])

    # Testy dla metody returning_goods()
    def test_returning_goods_returns_false_when_invoice_not_found(self):
        self.mock_repo.find_by_number.return_value = None
        result = self.shop.returning_goods(self.sample_invoice)
        self.assertFalse(result)

    def test_returning_goods_calls_warehouse_add_for_each_item(self):
        self.mock_repo.find_by_number.return_value = self.sample_invoice
        self.shop.returning_goods(self.sample_invoice)

        self.assertEqual(self.mock_warehouse.add_product.call_count, len(self.sample_invoice.items))

        calls = self.mock_warehouse.add_product.call_args_list
        for i, (product, quantity) in enumerate(self.sample_invoice.items):
            args, kwargs = calls[i]
            self.assertEqual(args[0], product)
            self.assertEqual(args[1], quantity)

    def test_returning_goods_calls_repository_delete(self):
        self.mock_repo.find_by_number.return_value = self.sample_invoice
        self.shop.returning_goods(self.sample_invoice)
        self.mock_repo.delete.assert_called_once_with(self.sample_invoice)

    def test_returning_goods_returns_true_when_successful(self):
        self.mock_repo.find_by_number.return_value = self.sample_invoice
        result = self.shop.returning_goods(self.sample_invoice)
        self.assertTrue(result)

    # Testy dla metody partial_return()
    def test_partial_return_raises_error_when_invoice_not_found(self):
        self.mock_repo.find_by_number.return_value = None
        with self.assertRaises(ValueError):
            self.shop.partial_return(1, [("cukierki", 1)])

    def test_partial_return_validates_items(self):
        self.mock_repo.find_by_number.return_value = self.sample_invoice

        with self.assertRaises(ValueError):
            self.shop.partial_return(1, [("mleko", 1)])

        with self.assertRaises(ValueError):
            self.shop.partial_return(1, [("cukierki", 3)])

    def test_partial_return_calls_warehouse_add_for_returned_items(self):
        self.mock_repo.find_by_number.return_value = self.sample_invoice
        items_to_return = [("cukierki", 1)]

        self.shop.partial_return(1, items_to_return)

        self.mock_warehouse.add_product.assert_called_once_with("cukierki", 1)

    def test_partial_return_updates_invoice_items(self):
        self.mock_repo.find_by_number.return_value = self.sample_invoice

        updated_invoice = self.shop.partial_return(1, [("cukierki", 1)])

        expected_items = [("cukierki", 1), ("chleb", 1)]
        self.assertEqual(updated_invoice.items, expected_items)

    def test_partial_return_calls_repository_update(self):
        self.mock_repo.find_by_number.return_value = self.sample_invoice
        self.shop.partial_return(1, [("cukierki", 1)])
        self.mock_repo.update.assert_called_once()

    def test_partial_return_removes_item_when_fully_returned(self):
        self.mock_repo.find_by_number.return_value = self.sample_invoice

        updated_invoice = self.shop.partial_return(1, [("chleb", 1)])

        expected_items = [("cukierki", 2)]
        self.assertEqual(updated_invoice.items, expected_items)

    def test_partial_return_handles_multiple_items(self):
        self.mock_repo.find_by_number.return_value = self.sample_invoice
        items_to_return = [("cukierki", 1), ("chleb", 1)]

        updated_invoice = self.shop.partial_return(1, items_to_return)

        expected_items = [("cukierki", 1)]
        self.assertEqual(updated_invoice.items, expected_items)

        self.assertEqual(self.mock_warehouse.add_product.call_count, 2)
        self.mock_warehouse.add_product.assert_any_call("cukierki", 1)
        self.mock_warehouse.add_product.assert_any_call("chleb", 1)


if __name__ == "__main__":
    unittest.main()