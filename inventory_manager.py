import json
from product import CanBeShipped
from product_factory import ProductFactory
from inventory import Inventory
from supplier import Supplier


def menu():
    print("--------MENU---------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory and suppliers")
    print("6. Add Supplies")
    print("7. Exit")

def load_inventory(suppliers):
    my_inventory = Inventory()
    try:
        with open('inventory.json', 'r') as file:
           data = json.load(file)
           print("inventory.json found")
           my_inventory.load_products(data["products"], suppliers)
           print("Inventory loaded successfully")

    except FileNotFoundError: 
        print("Warning: inventory.json not found. Returning empty inventory.")
    return my_inventory

def load_suppliers():
        suppliers: list[Supplier] = []
        try:
            with open("suppliers.json", "r") as file:
                data = json.load(file)
                print("suppliers.json found.")
                for supplier_data in data["suppliers"]:
                    supplier = Supplier(
                        supplier_data["supplier_id"],
                        supplier_data["name"],
                        supplier_data["contact_email"],
                )
                suppliers.append(supplier)
        except FileNotFoundError:
            print("suppliers.json not found. Using blank supplier list.")
        return suppliers

def save_suppliers(suppliers: list[Supplier]):
    suppliers_list: list[dict[str, str | float | int]] = []
    for supplier in suppliers:
        suppliers_list.append({
            "supplier_id": supplier.supplier_id,
            "name": supplier.name,
            "contact_email": supplier.contact_email,
        })
    with open("suppliers.json", "w") as file:
        suppliers_data = {"suppliers": suppliers_list}
        json.dump(suppliers_data, file, indent=4)
    print("Suppliers saved successfully to suppliers.json.")

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
menu()
print()

my_suppliers = load_suppliers()
my_inventory = load_inventory(my_suppliers)
option = int(input("Enter Option: "))
while option != 7:
    if option == 1:
        my_inventory.display_all()

    elif option == 2:
        try:
            id = input("Enter Product ID: ")
            name = input("Enter Product Name: ")
            price = float(input("Enter the price of the product: "))
            stock = int(input("Enter the stock quantity of the product: "))
            supplier_id = input("Enter the supplier ID: ")
            supplier = next((s for s in my_suppliers if s.supplier_id == supplier_id), None)

            if supplier is None:
                print("Supplier ID not found. Please add the supplier first.")
            else:
                product_type = input("Enter the type of product (Physical/Digital): ")
                if product_type == "Physical":
                    extra = {"weight": float(input("Enter the weight of the product: "))}
                elif product_type == "Digital":
                    extra = {"download_size": float(input("Enter the size of the downloadable product in MB: "))}
                else:
                    extra = None
                    print("Invalid product type.")

                if extra is not None:
                    item = ProductFactory.create(product_type, id, name, price, stock, supplier, **extra)
                if isinstance(item, CanBeShipped):
                    print(f"Shipping Cost: {item.calculate_shipping_cost()}")
                if my_inventory.add_product(item):
                    print("Added product to inventory!")       
        except ValueError as e:
            print(f"Could not add product: {e}")

    elif option == 3:
        id = input("Enter Product ID: ")
        product_obj = my_inventory.find_product(id)
        if product_obj is not None:
            try:
                new_stock = int(input("What is the stock amount you will like to update to: "))
                product_obj.update_stock(new_stock)
                print("Stock updated successfully!")
            except ValueError as e:
                print(f"Stock not updated: {e}")
        else:
            print("Product ID not found")

    elif option == 4:
        id = input("Enter Product ID you are searching for : ")
        my_inventory.find_product(id)

    elif option == 5:
        print("Saving inventory and supliers....")
        save_inventory(my_inventory)
        save_suppliers(my_suppliers)

    elif option == 6:
        supplier_id = input("Supplier ID: ")
        supplier_name = input("Supplier Name: ")
        supplier_email = input("Supplier Contact Email: ")
        supplier = Supplier(supplier_id,supplier_name,supplier_email)
        print("Supplier added successfully")
        my_suppliers.append(supplier)
    else:
        print("Invalid option, Please choose between 1 and 6.")
    
    print()
    menu()
    option = int(input("Enter Option: ")) 
    print()

print("Saving inventory and supplier lsit before exit....")
save_inventory(my_inventory)
save_suppliers(my_suppliers)

print("Thank You for using Inventory Management System")
print("Program terminated")
