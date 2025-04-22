class ShoppingAssistance:
    def __init__(self):
        self.products = {
            "electronics": ["Smartphone", "Laptop", "Headphones"],
            "clothing": ["T-shirt", "Jeans", "Jacket"],
            "home": ["Cookware", "Lamp", "Cushions"]
        }
        self.preference = None

    def user_preference(self):
        print("Please enter your shopping preference (electronics/clothing/home):")
        self.preference = input("Your preference: ").lower()

    def recommend_user(self):
        if self.preference in self.products:
            print(f"\nRecommended products in {self.preference}:")
            for item in self.products[self.preference]:
                print(f"- {item}")
        else:
            print("Sorry, we don't have recommendations for that category.")

assistant = ShoppingAssistance()
assistant.user_preference()
assistant.recommend_user()
