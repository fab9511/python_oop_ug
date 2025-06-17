from Shop import Shop
from Warehouse import Warehouse
from InvoiceRepository import InvoiceRepository


class ShopSystem:
    def __init__(self):
        self.warehouse = Warehouse({
            "Jabłka": [100, 2.5],
            "Banany": [80, 3.0],
            "Pomarańcze": [50, 4.0]
        })
        self.invoice_repo = InvoiceRepository()
        self.shop = Shop(self.invoice_repo, self.warehouse)
        self.cart = []  # Koszyk na produkty
        self.current_customer = ""

    @staticmethod
    def display_main_menu():
        print("\n=== SYSTEM SKLEPOWY ===")
        print("1. Dodaj produkt do magazynu")
        print("2. Pokaż stan magazynu")
        print("3. Wystaw fakturę (kup produkty)")
        print("4. Pokaż faktury")
        print("5. Dokonaj zwrotu")
        print("6. Wyjście")
        choice = input("Wybierz opcję (1-6): ")
        return choice

    def add_product_to_warehouse(self):
        print("\n--- DODAWANIE PRODUKTU DO MAGAZYNU ---")
        name = input("Nazwa produktu: ").strip()

        while True:
            try:
                quantity = int(input("Ilość: "))
                if quantity <= 0:
                    print("Ilość musi być dodatnia!")
                    continue
                break
            except ValueError:
                print("Nieprawidłowa ilość! Wprowadź liczbę.")

        while True:
            try:
                price = float(input("Cena za sztukę: "))
                if price <= 0:
                    print("Cena musi być dodatnia!")
                    continue
                break
            except ValueError:
                print("Nieprawidłowa cena! Wprowadź liczbę.")

        try:
            self.warehouse.add_product(name, quantity, price)
            print(f"\n✅ Dodano do magazynu: {name} ({quantity} szt.) po {price} zł/szt")
        except Exception as e:
            print(f"\n❌ Błąd: {e}")

    def show_inventory(self):
        print("\n--- STAN MAGAZYNU ---")
        if not self.warehouse.products:
            print("Magazyn jest pusty")
            return

        print(f"{'Produkt':<15} {'Ilość':<10} {'Cena':<10}")
        print("-" * 35)
        for product, (qty, price) in self.warehouse.products.items():
            print(f"{product:<15} {qty:<10} {price:.2f} zł/szt")

    def add_to_cart(self):
        print("\n--- DODAWANIE PRODUKTÓW DO FAKTURY ---")
        self.show_inventory()

        name = input("\nPodaj nazwę produktu (lub wpisz 'koniec' aby zakończyć): ").strip()
        if name.lower() == 'koniec':
            return False

        if name not in self.warehouse.products:
            print("❌ Produkt nie istnieje w magazynie!")
            return True

        try:
            max_qty = self.warehouse.products[name][0]
            qty = int(input(f"Ilość (dostępne: {max_qty}): "))

            if qty <= 0:
                print("Ilość musi być dodatnia!")
                return True
            if qty > max_qty:
                print(f"❌ Niedostępna ilość! Maksymalnie: {max_qty}")
                return True

            self.cart.append((name, qty))
            print(f"✅ Dodano do faktury: {name} ({qty} szt.)")
            return True
        except ValueError:
            print("❌ Nieprawidłowa ilość!")
            return True

    def create_invoice(self):
        print("\n--- WYSTAWIENIE NOWEJ FAKTURY ---")

        if not self.current_customer:
            self.current_customer = input("Imię i nazwisko klienta: ").strip()

        self.cart = []
        while self.add_to_cart():
            pass

        if not self.cart:
            print("❌ Anulowano - brak produktów w fakturze")
            return

        print("\nPodsumowanie faktury:")
        print(f"Klient: {self.current_customer}")
        total = 0
        for name, qty in self.cart:
            price = self.warehouse.products[name][1]
            item_total = price * qty
            print(f"- {name}: {qty} szt. × {price:.2f} zł = {item_total:.2f} zł")
            total += item_total

        print(f"\nSUMA: {total:.2f} zł")

        confirm = input("\nCzy wystawić fakturę? (t/n): ").lower()
        if confirm == 't':
            try:
                invoice = self.shop.buy(self.current_customer, self.cart)
                print(f"\n✅ Wystawiono fakturę nr {invoice.number}")
                self.cart = []
                self.current_customer = ""
            except Exception as e:
                print(f"\n❌ Błąd przy wystawianiu faktury: {e}")
        else:
            print("❌ Anulowano wystawienie faktury")

    def show_invoices(self):
        print("\n--- LISTA FAKTUR ---")
        invoices = self.invoice_repo.data_source

        if not invoices:
            print("Brak wystawionych faktur")
            return

        for invoice in invoices:
            print(f"\nFaktura nr {invoice.number}")
            print(f"Klient: {invoice.customer}")
            print("Produkty:")
            for product, quantity in invoice.items:
                print(f"- {product}: {quantity} szt.")

        input("\nNaciśnij Enter, aby kontynuować...")

    def process_return(self):
        print("\n--- ZWROT TOWARU ---")
        self.show_invoices()

        if not self.invoice_repo.data_source:
            return

        try:
            invoice_num = input("\nPodaj numer faktury do zwrotu: ").strip()
            invoice = self.invoice_repo.find_by_number(int(invoice_num))

            if not invoice:
                print("❌ Nie znaleziono faktury o podanym numerze")
                return

            print(f"\nFaktura nr {invoice.number} dla {invoice.customer}")
            print("Produkty na fakturze:")
            for i, (product, quantity) in enumerate(invoice.items, 1):
                print(f"{i}. {product}: {quantity} szt.")

            return_type = input("\nZwrot całościowy (c) czy częściowy (z)? ").lower()

            if return_type == 'c':
                if self.shop.returning_goods(invoice):
                    print("✅ Zwrócono całość towaru i anulowano fakturę")
                else:
                    print("❌ Nie udało się dokonać zwrotu")
            elif return_type == 'z':
                items_to_return = []
                while True:
                    try:
                        item_num = input("\nPodaj numer produktu do zwrotu (lub 'koniec'): ")
                        if item_num.lower() == 'koniec':
                            break

                        item_idx = int(item_num) - 1
                        if item_idx < 0 or item_idx >= len(invoice.items):
                            print("❌ Nieprawidłowy numer produktu")
                            continue

                        product, max_qty = invoice.items[item_idx]
                        qty = int(input(f"Ilość do zwrotu (max {max_qty}): "))

                        if qty <= 0:
                            print("❌ Ilość musi być dodatnia")
                            continue
                        if qty > max_qty:
                            print(f"❌ Nie można zwrócić więcej niż {max_qty} szt.")
                            continue

                        items_to_return.append((product, qty))
                        print(f"✅ Dodano do zwrotu: {product} ({qty} szt.)")
                    except (ValueError, IndexError):
                        print("❌ Nieprawidłowe dane")

                if items_to_return:
                    try:
                        self.shop.partial_return(invoice.number, items_to_return)
                        print("\n✅ Dokonano częściowego zwrotu")
                    except Exception as e:
                        print(f"\n❌ Błąd przy zwrocie: {e}")
                else:
                    print("❌ Anulowano zwrot - brak produktów")
            else:
                print("❌ Nieprawidłowy wybór")
        except ValueError:
            print("❌ Nieprawidłowy numer faktury")

    def run(self):
        while True:
            choice = self.display_main_menu()

            if choice == '1':
                self.add_product_to_warehouse()
            elif choice == '2':
                self.show_inventory()
            elif choice == '3':
                self.create_invoice()
            elif choice == '4':
                self.show_invoices()
            elif choice == '5':
                self.process_return()
            elif choice == '6':
                print("\nDziękujemy za korzystanie z systemu!")
                break
            else:
                print("❌ Nieprawidłowy wybór. Spróbuj ponownie.")


