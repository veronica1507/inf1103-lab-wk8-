import json

def menu():
    print("--------MENU---------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")

def load_inventory():
    try:
        with open('inventory.json', 'r') as file:
           data = json.load(file)
        print("inventory.json found")
        print("Inventory loaded successfully")
        return data
    except FileNotFoundError: 
        print("Warning: inventory.json not found. Returning empty inventory.")
        return {}

def save_inventory(inventory):
    with open('inventory.json', 'w') as file:
            json.dump(inventory, file, indent=4)
    print("Saving inventory.....")
    print("Inventory saved successfully to inventory.json")

def display_all(inventory):
    print("Current Inventory")
    print("-" * 50)
    inventory_list = inventory["products"]  #Access the list inside 'products'
    for product in inventory_list:
        id = product["ID"]
        name = product["Name"]
        price = product["Price"]
        stock = product ["Stock"]
        print(f"ID: {id} | Name: {name} | Price: {price} | Stock: {stock} ")
    print("-" * 50)

def add_stock(inventory):
    item_id = input("Product ID: ")
    product_name = input("Product Name: ")
    price = float(input("Price: "))
    stock = int(input("Stock Quantity: "))

    new_product = {
        "ID": item_id,
        "Name": product_name,
        "Price": price,
        "Stock": stock
    }

    inventory["products"].append(new_product)
    print("Product added successfully !")

def update_stock(inventory):
    item_id = input("Product ID: ")
    inventory_list = inventory["products"]
    for product in inventory_list:
        if item_id == product["ID"]:
            print("Product Found")
            name = product["Name"]
            stock = product ["Stock"]
            print(f"Name: {name}")
            print(f"Current stock: {stock}")
            new_stock = int(input("New Stock Quantity: "))
            product['Stock'] = new_stock
            print("Stock updated successfully")

        else:
            print("Not found")

def search_product(inventory):
    item_id = input("Product ID: ")
    inventory_list = inventory["products"]
    for product in inventory_list:
        if item_id == product["ID"]:
            print("Product Found")
            print("-" * 50)
            id = product["ID"]
            name = product["Name"]
            price = product["Price"]
            stock = product ["Stock"]
            print(f"ID: {id}")
            print(f"Name: {name}")
            print(f"Price: {price}")
            print(f"Stock: {stock}")
            print("-" * 50)
        else:
            print("Product not found")


print("============================")
print("INVENTORY MANAGEMENT SYSTEM")
print("============================")
print()
inventory = load_inventory()
print()
menu()
print()
option = int(input("Enter Option: "))
while option != 6:
    if option == 1:
        display_all(inventory)
    elif option == 2:
        add_stock(inventory)
    elif option == 3:
        update_stock(inventory)
    elif option == 4:
        search_product(inventory)
    else:
        save_inventory(inventory)

    option = int(input("Enter Option: ")) 

print("Saving inventory before exit....")
save_inventory(inventory)
print("Thank You for using Inventory Management System")
print("Program terminated")
