class TouristSystem:
    def __init__(self):
        self.destinations = {
            "Paris": {
                "country": "France",
                "attractions": ["Eiffel Tower", "Louvre Museum", "Seine River Cruise"]
            },
            "Tokyo": {
                "country": "Japan",
                "attractions": ["Tokyo Tower", "Shibuya Crossing", "Sensoji Temple"]
            },
            "New York": {
                "country": "USA",
                "attractions": ["Statue of Liberty", "Central Park", "Times Square"]
            }
        }

    def show_destinations(self):
        print("Available Destinations:")
        for city in self.destinations:
            print(f"- {city}")

    def get_info(self, city):
        city = city.title()
        if city in self.destinations:
            data = self.destinations[city]
            print(f"\n📍 {city}, {data['country']}")
            print("Top Attractions:")
            for attraction in data["attractions"]:
                print(f"✔ {attraction}")
        else:
            print("❌ Destination not found.")

# Sample Run
tourist = TouristSystem()
tourist.show_destinations()
tourist.get_info("Tokyo")  # You can change this to Paris or New York
