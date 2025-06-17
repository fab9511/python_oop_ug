# products = dict(product: [ilosc, cena_za_sztuke])
class OutOfStore(Exception):
    pass


class Warehouse:
                    #products = dict(product_name: [quantity, price_per_unit])
    def __init__(self, products=dict()):
        self.products = products

    def add_product(self, product, number, price_per_unit=None):
            if product not in self.products:
                if price_per_unit is None:
                    raise ValueError("Price must be provided for new product")
                self.products[product] = [number, price_per_unit]
            else:
                self.products[product][0] += number
                if price_per_unit is not None:
                    self.products[product][1] = price_per_unit

    def remove_product(self, product, number):
        if product not in self.products:
            raise Exception(f"Product '{product}' not found")

        current_quantity = self.products[product][0]

        if current_quantity == number:
            self.products.pop(product)
        elif current_quantity > number:
            self.products[product][0] -= number
        else:
            raise OutOfStore(f"Not enough '{product}' in warehouse. "
                             f"Available: {current_quantity}, requested: {number}")




