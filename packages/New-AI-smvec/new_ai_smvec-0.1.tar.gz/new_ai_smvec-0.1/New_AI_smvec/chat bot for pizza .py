class Pizza:
    def __init__(self, name, price):
        self.name = name
        self.price = price

class PizzeriaChatbot:
    def __init__(self):
        self.menu = [
            Pizza("Margherita", 250),
            Pizza("Farmhouse", 350),
            Pizza("Peppy Paneer", 400),
            Pizza("Veg Extravaganza", 450)
        ]
        self.order = []

    def show_menu(self):
        print("\n🍕 Welcome to AI Pizzeria!")
        print("Here's our menu:")
        for idx, pizza in enumerate(self.menu, start=1):
            print(f"{idx}. {pizza.name} - ₹{pizza.price}")

    def take_order(self, choice):
        if 1 <= choice <= len(self.menu):
            selected = self.menu[choice - 1]
            self.order.append(selected)
            print(f"✅ Added {selected.name} to your order.")
        else:
            print("❌ Invalid choice.")

    def show_order_summary(self):
        print("\n🧾 Your Order Summary:")
        total = 0
        for pizza in self.order:
            print(f"- {pizza.name} - ₹{pizza.price}")
            total += pizza.price
        print(f"Total: ₹{total}")
        print("🎉 Thank you for ordering! Your pizza will arrive soon.")

bot = PizzeriaChatbot()
bot.show_menu()
bot.take_order(1)  # Ordering Margherita
bot.take_order(3)  # Ordering Peppy Paneer
bot.show_order_summary()
