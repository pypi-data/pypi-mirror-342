class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

class MWallet:
    def __init__(self, balance=0):
        self.balance = balance

    def add_money(self, amount):
        self.balance += amount
        print(f"₹{amount} added to wallet. Current balance: ₹{self.balance}")

    def make_payment(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            print(f"Payment of ₹{amount} successful. Remaining balance: ₹{self.balance}")
            return True
        else:
            print("Insufficient balance in M-Wallet.")
            return False

class OnlineShop:
    def __init__(self):
        self.products = [
            Product("Shoes", 1500),
            Product("T-shirt", 800),
            Product("Watch", 2000)
        ]
        self.wallet = MWallet()

    def show_products(self):
        print("\nAvailable Products:")
        for idx, product in enumerate(self.products, start=1):
            print(f"{idx}. {product.name} - ₹{product.price}")

    def buy_product(self, choice):
        if 1 <= choice <= len(self.products):
            product = self.products[choice - 1]
            print(f"You selected: {product.name}")
            if self.wallet.make_payment(product.price):
                print("Order placed successfully!")
        else:
            print("Invalid product selection.")

# Sample run
shop = OnlineShop()
shop.wallet.add_money(3000)     # Add money to wallet
shop.show_products()            # Display products
shop.buy_product(2)             # Buy product 2 (T-shirt)
