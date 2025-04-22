class AutomationSystem:
    def __init__(self, name, category, rating, is_active=True):
        self.name = name                
        self.category = category        
        self.rating = rating            
        self.is_active = is_active

    def display_info(self):
        status = "Active" if self.is_active else "Inactive"
        print(f"🔹 Automation System: {self.name}")
        print(f"📂 Category         : {self.category}")
        print(f"⭐ Rating           : {self.rating}/5")
        print(f"🔘 Status           : {status}")

    def deactivate(self):
        self.is_active = False
        print(f"❌ {self.name} has been deactivated.")

    def activate(self):
        self.is_active = True
        print(f"✅ {self.name} is now active.")
