# Import tabulate module.
from tabulate import tabulate
#========The beginning of the class==========
class Shoe:

    def __init__(self, country, code, product, cost, quantity):
        '''
        In this function, you must initialise the following attributes:
            ● country,
            ● code,
            ● product,
            ● cost, and
            ● quantity.
        '''
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    def get_cost(self):
        '''
        Add the code to return the cost of the shoe in this method.
        '''
        return self.cost

    def get_quantity(self):
        '''
        Add the code to return the quantity of the shoes.
        '''
        return self.quantity

    def __str__(self):
        '''
        Add a code to return a string representation of a class.
        '''
        return f'''{self.country}, {self.code}, {self.product}, {self.cost}, 
        {self.quantity}'''



#=============Shoe list===========
'''
The list will be used to store a list of objects of shoes.
'''
shoe_list = []


#==========Functions outside the class==============
def read_shoes_data():
    '''
    This function will open the file inventory.txt
    and read the data from this file, then create a shoes object with this data
    and append this object into the shoes list. One line in this file 
    represents data to create one object of shoes. You must use the try-except
    in this function for error handling. Remember to skip the first line using
    your code.
    '''
    try:
        with open("inventory.txt", "r") as file:
            # Skipping the first line
            next(file)

            # Create a Shoe object with the data and append to the global list.
            for line in file:
                country, code, product, cost, quantity = line.strip().split(",")
                cost = float(cost)  # Convert cost to float
                quantity = int(quantity)  # Convert quantity to int
                shoe = Shoe(country, code, product, cost, quantity)
                shoe_list.append(shoe)

    # Print error message if the file is not found.            
    except FileNotFoundError:
        print("Error, file not found.")
    except Exception as e:
        print(f"An error occurred: {e}")



def capture_shoes():
    '''
    This function will allow a user to capture data
    about a shoe and use this data to create a shoe object
    and append this object inside the shoe list.
    '''
    print("Capture shoe data")
    country = input("Enter the country: ")
    code = input("Enter the code: ")

    # Check if the shoe code already exists
    for shoe in shoe_list:
        if shoe.code == code:
            print("Error: Shoe code already exists. Please enter a unique code.")
            return

    product = input("Enter the product: ")

    # Use while loop to ensure the user enters valid values for cost and 
    # Quantity.
    while True:
        try:
            cost = int(input("Enter the cost: "))
            quantity = int(input("Enter the quantity: "))
            if cost <= 0 or quantity <= 0:
                print("Error, please enter a valid value greater than 0!")
                continue

            # Create a shoe object with the correct data and append to the 
            # 'shoe_list'.
            captured_shoe = Shoe(country, code, product, cost, quantity)
            shoe_list.append(captured_shoe)
            
            # Append the captured shoe to 'inventory.txt'.
            with open("inventory.txt", "a") as file:
                file.write(f"\n{captured_shoe}")
                print("\nProcess complete, Shoes successfully added.")
                break
        
        except ValueError:
            print("\nInvalid input, please enter whole numbers.")




def view_all():
    '''
    This function will iterate over the shoes list and
    print the details of the shoes returned from the __str__
    function. Optional: you can organise your data in a table format
    by using Python’s tabulate module.
    '''
    # To organise the data in a table format.
    head = ["Country", "Code", "Product", "Cost", "Quantity"]

    # Create a list of lists using list comprehension.
    view_all = [
        [shoe.country, shoe.code, shoe.product, shoe.cost, shoe.quantity]
        for shoe in shoe_list
    ]

    print("\nStock Details: ")
    print(tabulate(view_all, headers=head, tablefmt="plain"))


def re_stock():
    '''
    This function will find the shoe object with the lowest quantity,
    which is the shoes that need to be re-stocked. Ask the user if they
    want to add this quantity of shoes and then update it.
    This quantity should be updated on the file for this shoe.
    '''
    # Create an empty list to store the quantity of each shoe.
    stock = []

    # Loop through the list of shoes and use get_quantity and append to list.
    # Determine the lowest quantity by using the min() function.
    for shoe in shoe_list:
        quantity = shoe.get_quantity()
        stock.append(quantity)
    min_qty = min(stock)

    shoes_to_restock = None
    for shoe in shoe_list:
        if shoe.get_quantity() == min_qty:
            shoes_to_restock = shoe
            break

    # Provide details of the low_stock
    print("\nLow Stock: ")
    head = ["Country", "Code", "Product", "Cost", "Quantity"]
    print(tabulate(
    [[shoes_to_restock.country, shoes_to_restock.code, shoes_to_restock.product,
      shoes_to_restock.cost, shoes_to_restock.quantity]],
    headers=head, tablefmt="plain"
                    ))


    # Ensure that the user enters a valid value.
    # Else display an error message.
    while True:
        try:
            restock_qty = int(input("\nEnter the quantity to restock: "))
            if restock_qty > 0:
                shoes_to_restock.quantity += restock_qty
                print("\nStock update successful")
                break
            else:
                print("Enter a value greater than 0.")

        except ValueError:
            print("Error! Value needs to be a whole number.")

    # Open "inventory.txt" and read from it.
    with open("inventory.txt", "r") as file:
        contents = file.readlines()

    # Open "inventory.txt" for writing.
    # Use for loop to update the current stock in the file.
    with open("inventory.txt", "w") as file:
        for line in contents:
            list = line.strip().split(",")
            if list[1] == shoes_to_restock.code:
                file.write(f'''{shoes_to_restock.country},
                           {shoes_to_restock.code},{shoes_to_restock.product},
                           {shoes_to_restock.cost},{shoes_to_restock.quantity}
                            \n''')
            else:
                file.write(line)
 

def search_shoe():
    '''
    This function will search for a shoe from the list
    using the shoe code and return this object so that it will be printed.
    '''
    try:
        search_code = input("Enter the shoe code to search: ").strip()
        if not search_code:
            print("Error: Shoe code cannot be empty.")
            return

        found = False
        for shoe in shoe_list:
            if shoe.code.strip() == search_code:
                print(shoe)
                found = True
                break

        if not found:
            print("Shoe not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def value_per_item():
    '''
    This function will calculate the total value for each item.
    Please keep the formula for value in mind: value = cost * quantity.
    Print this information on the console for all the shoes.
    '''
    for shoe in shoe_list:
        # Ensure cost and quantity are of the correct data types
        cost = float(shoe.cost)
        quantity = int(shoe.quantity)
        total_value = cost * quantity
        print(f"Shoe: {shoe.product}\nTotal Value: R{total_value:.2f}\n")


def highest_qty():
    '''
    Write code to determine the product with the highest quantity and
    print this shoe as being for sale.
    '''
    # Create a list to store quantities.
    quantities = [shoe.get_quantity() for shoe in shoe_list]

    # Determine the highest quantity.
    highest_quantity = max(quantities)

    # Find the shoe with the highest quantity.
    shoes_on_sale = None
    for shoe in shoe_list:
        if shoe.get_quantity() == highest_quantity:
            shoes_on_sale = shoe
            break

    # Display shoe with highest quantity as for sale in table form.
    print("Shoe for sale: ")
    head = ["Country", "Code", "Product", "Cost", "Quantity"]
    print(tabulate(
    [[shoes_on_sale.country, shoes_on_sale.code, shoes_on_sale.product,
      shoes_on_sale.cost, shoes_on_sale.quantity]],
    headers=head, tablefmt="plain"
                    ))



#==========Main Menu=============
'''
Create a menu that executes each function above.
This menu should be inside the while loop. Be creative!
'''
# Menu function.
def main_menu():
    
    while True:
        shoe_list.clear()
        read_shoes_data()

        print("\nThis is a Shoe Inventory Management System")
        print("1. View all stock details")
        print("2. Search for a shoe by code")
        print("3. View total value of each shoe item")
        print("4. View shoes that are low on stock to re-stock")
        print("5. View items that are on sale(highest quantity shoe)")
        print("6. Capture new shoe and add to the stock list")
        print("0. Exit")


        choice = input("Select a number from the menu above: ")

        if choice == "1":
            view_all()
        elif choice == "2":
            search_shoe()
        elif choice == "3":
            value_per_item()
        elif choice == "4":
            re_stock()
        elif choice == "5":
            highest_qty()
        elif choice == "6":
            capture_shoes()
        elif choice == "0":
            print("Goodbye.")
            exit()
        else:
            print("Invalid choice!")
    
# Initialize the menu.
main_menu()