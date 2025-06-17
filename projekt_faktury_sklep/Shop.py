from abc import ABC
from Invoice import Invoice
from Warehouse import Warehouse


class Shop(ABC):
    def __init__(self, repository=None, warehouse=None):
        self.__invoice_repository = repository
        self.__warehouse = warehouse

    @property
    def warehouse(self):
        return self.__warehouse
    @property
    def invoice_repository(self):
        return self.__invoice_repository

    def buy(self, customer, items_list):
        for product, quantity in items_list:
            self.warehouse.remove_product(product, quantity)

        invoice = Invoice(number=self.invoice_repository.get_next_number(), customer=customer, items=items_list)
        self.invoice_repository.add(invoice)
        return invoice

    def returning_goods(self, invoice):
        if self.invoice_repository.find_by_number(invoice.number):
            for product, quantity in invoice.items:
                self.warehouse.add_product(product, quantity)
            self.invoice_repository.delete(invoice)
            return True
        else:
            return False

    def _get_invoice_or_raise(self, invoice_number):
        invoice = self.invoice_repository.find_by_number(invoice_number)
        if not invoice:
            raise ValueError("Invoice not found")
        return invoice

    @staticmethod
    def _convert_items_to_dict(items):
        return {product: quantity for product, quantity in items}

    @staticmethod
    def _validate_items_to_return(current_items, items_to_return_dict):
        for product, quantity in items_to_return_dict.items():
            if product not in current_items:
                raise ValueError(f"Product '{product}' not in invoice")
            if quantity > current_items[product]:
                raise ValueError(f"Cannot return {quantity} of '{product}', only {current_items[product]} available")

    def _process_return(self, current_items, items_to_return_dict):
        new_items = []
        for product, quantity in current_items.items():
            if product in items_to_return_dict:
                returned_quantity = items_to_return_dict[product]
                new_quantity = quantity - returned_quantity
                if new_quantity > 0:
                    new_items.append((product, new_quantity))
                self.warehouse.add_product(product, returned_quantity)
            else:
                new_items.append((product, quantity))
        return new_items

    def partial_return(self, invoice_number, items_to_return):
        invoice = self._get_invoice_or_raise(invoice_number)
        current_items = self._convert_items_to_dict(invoice.items)
        items_to_return_dict = dict(items_to_return)

        self._validate_items_to_return(current_items, items_to_return_dict)

        new_items = self._process_return(current_items, items_to_return_dict)
        invoice.items = new_items

        self.invoice_repository.update(invoice)
        return invoice



