import csv

class MenuItem:
    def __init__(self, name, price):
        self.name = name
        self.price = price

class Menu:
    def __init__(self):
        self.foods = []

    def add_food(self, food):
        self.foods.append(food)

    def display_menu(self):
        print("Menu:")
        for food in self.foods:
            print(f"{food.name}: ${food.price}")

    def find_food(self, keyword):
        matches = []
        for food in self.foods:
            if keyword.lower() in food.name.lower():
                matches.append(food)
        return matches

    def read_menu_from_csv(self, file_path):
        with open(file_path, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                name = row['Item']
                price = float(row['Price'].replace('$', '').strip())
                food = MenuItem(name, price)
                self.add_food(food)

class Restaurant:
    def __init__(self, name= "Whatever you want", waiter = None):
        self.name = name
        self.waiter = waiter

    def welcome_guest(self):
        print(f"Welcome to {self.name}!")

    def ask_party_size(self):
        self.waiter.party_size = int(input("How many guests are in your party today?"))

    def ask_waiter_to_serve(self):
        self.waiter.assign_guests(self.waiter.party_size)
    
    def update_tables(self):
        print("Updated table assignments:", self.waiter.restaurant_tables)
    
    def book_table(self, table_number):
        if table_number in self.waiter.restaurant_tables:
            if self.waiter.restaurant_tables[table_number] >0:
                print(f"Table {table_number} has been reserved.")
                self.waiter.restaurant_tables[table_number] = 0 
            else:
                print(f"sorry, table{table_number} is not available.")
        else:
             print("Invalid table number.")
     
    def __str__(self):
        return f"Restaurant: {self.name}, Waiter: {self.waiter}"

        
class Waiter:
    
    """Initialize a class representing a waiter in a restaurant."""
    
    def __init__(self, restaurant_tables):
        
        """Args: 
            restaurant_tables (dict): An dictionary containing restaurant tables and their seating capacity.
            
            party_size (int): An integer of input of the amount of guests per party.
            
            Menu: A class containing menuitems.
        """
        
        
        self.restaurant_tables = restaurant_tables
        self.party_size = 0
        self.menu = Menu()

    def assign_guests(self, num_guests):
        
        """Initializes a method that assigns guests to a table according to their party size and table capacity.
        
            Args:
                num_guests (int): number of guests per party.
            
            Side effects: 
                Modifies the value of num_guests and assigning a table according to party size..
                
            Returns: 
                Returns f-string saying how many guests are assgined to which table. """
        
        assigned = False
        for table, capacity in self.restaurant_tables.items():
            if num_guests <= capacity:
                self.restaurant_tables[table] -= num_guests
                print(f"Assigned {num_guests} guests to table {table}.")
                assigned = True
                break
        if not assigned:
            print("No available table to accommodate the guests.")

restaurant_tables = {
    1: 2,
    2: 4,
    3: 6,
    4: 8,
    5: 10
}

def take_orders(customer_info, menu):
    orders = {}
    for person, party_size in customer_info:
        print(f'Ordering for party of {party_size} ({person}):')
        orders[person] = []
        for i in range(party_size):
            print(f'Ordering for person {i+1}:')
            order = input('What would you like to eat today? ')
            matches = menu.find_food(order)
            if matches:
                print(f'Menu items matching "{order}":')
                for match in matches:
                    print(match.name)
                waiter = input("Please choose an item you would like to eat: ")
                orders[person].append(waiter)
            else:
                print("Sorry, we don't have that item on the menu, please choose something else.")
                orders[person].append(None)
    return orders

def billcalc(orders, menu):
    bill = {}
    sorted_menu = sorted(menu.foods, key=lambda x: x.price)
    for person, order_list in orders.items():
        total_price = 0
        for item in order_list:
            if item:
                for food in sorted_menu:
                    if item == food.name:
                        total_price += food.price
                        break
        bill[person] = total_price
    return bill

def main():
    # Create an instance of the Waiter class
    waiter = Waiter(restaurant_tables)

    # Create an instance of the Restaurant class
    restaurant = Restaurant("J.J.K.N Grill & Buffet", waiter)

    # Welcome the guests
    restaurant.welcome_guest()

    # Ask if the user wants to dine in or make a reservation
    choice = input("Are you dining in today? (yes/no): ").lower()

    if choice == "yes":
        # Ask for the party size
        restaurant.ask_party_size()

        # Ask the waiter to serve the guests
        restaurant.ask_waiter_to_serve()
        
        # Update tables seating 
        restaurant.update_tables()

        # Read menu from CSV
        menu = Menu()
        menu.read_menu_from_csv("bigmenu.csv")

        # Display the menu
        menu.display_menu()

        # Take orders after displaying the menu
        customer_info = [("Customer", waiter.party_size)]
        orders = take_orders(customer_info, menu)

        # Calculate bills
        bills = billcalc(orders, menu)

        # Print bills
        print("Bills:")
        for person, bill in bills.items():
            print(f"{person}: ${bill}")

    elif choice == "no":
        # Online Booking
        print("\nRESERVATION BOOKING:")
        date_input = input("What date would you like to book for? (DD/MM/YYYY): ")

        # Book tables
        print("\nReserve a Table:")
        table_to_book = int(input("Enter the table number you want to reserve (1-5): "))
        restaurant.book_table(table_to_book)

    else:
        print("Invalid choice. Please enter 'yes' or 'no'.")

    # Thank the guests for dining
    print("Thank you for dining in our restaurant!")

if __name__ == "__main__":
    main()
