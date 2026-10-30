import json
from product import Product , PhysicalProduct
from inventory import Inventory


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
        return []

def save_inventory(inventory_obj):
    data = inventory_obj.get_all_products_dict()
    with open('inventory.json', 'w') as file:
            json.dump(data, file, indent=4)
    print("Saving inventory.....")
    print("Inventory saved successfully to inventory.json")

print("============================")
print("INVENTORY MANAGEMENT SYSTEM")
print("============================")
print()
raw_data = load_inventory()
my_inventory = Inventory()
for item in raw_data:
    product_obj = Product(item['product_id'], item['name'], item ['price'], item['stock'])
    my_inventory.add_product(product_obj)

print()
menu()
print()
option = int(input("Enter Option: "))
while option != 6:
    if option == 1:
        my_inventory.display_all()
    elif option == 2:
        product_type = input("Enter the type of product ? (Physical/Digital): ")
        if product_type == "Physical":
                    weight = float(input("Enter the weight of the product: "))
                    
        id = input("Enter Product ID: ")
        name = input ("Enter Product Name: ")
        price = float(input("Enter ther price of the product:"))
        stock = int(input("Enter the stock quantity of the product: "))
        item = PhysicalProduct(id,name,price,stock,weight)  
        my_inventory.add_product(item)
        print("Added product to inventory!")
    
    elif option == 3:
        id = input("Enter Product ID: ")
        product_obj = my_inventory.search_product(id)
        if product_obj is not None:
            new_stock = int(input("What is the stock amount you will like to update to: "))
            product_obj.update_stock(new_stock)
            print("Stock updated successfully!")
        else:
            print("Product ID not found")

    elif option == 4:
        id = input("Enter Product ID you are searching for : ")
        my_inventory.search_product(id)

    elif option == 5:
        save_inventory(my_inventory)

    else:
        print("Invalid option, Please choose between 1 and 6.")
    
    print()
    menu()
    option = int(input("Enter Option: ")) 
    print()

print("Saving inventory before exit....")
save_inventory(my_inventory)
print("Thank You for using Inventory Management System")
print("Program terminated")
