import io
import inspect
import os
import sys
import tempfile
from contextlib import redirect_stdout
from unittest.mock import patch

PROJECT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT)          # so imports still work after changing folder

from supplier import Supplier
from product import PhysicalProduct, DigitalProduct
from product_factory import ProductFactory
from OrderLine import OrderLine
from order import Order
from discount import (DiscountStrategy, NoDiscount, PercentageDiscount,
                      BulkDiscount, StudentDiscount)
from inventory import Inventory

# Import inventory_manager without touching its menu code.
# The fake input "7" makes the menu exit immediately, and the exit-time save
# goes into a throwaway folder instead of your project folder.
original_dir = os.getcwd()
with tempfile.TemporaryDirectory() as scratch:
    os.chdir(scratch)
    try:
        with patch("builtins.input", side_effect=["7"]), redirect_stdout(io.StringIO()):
            import inventory_manager
    finally:
        os.chdir(original_dir)

get_positive_float = inventory_manager.get_positive_float
load_products = inventory_manager.load_products

passed = 0
failed = 0


def check(description, condition):
    global passed, failed
    if condition:
        passed += 1
        print(f"PASS: {description}")
    else:
        failed += 1
        print(f"FAIL: {description}")


def raises_value_error(function, *args, **kwargs):
    """Return the error message if ValueError is raised, otherwise None."""
    try:
        function(*args, **kwargs)
    except ValueError as e:
        return str(e)
    return None


supplier = Supplier("S1", "Test Supplier", "test@example.com")


def make_order(strategy=None):
    product = ProductFactory.create("Physical", "P1", "Mug", 50.0, 10,
                                    supplier, weight=0.4)
    order = Order("O1", strategy) if strategy else Order("O1")
    order.add_order_line(product, 2)          # subtotal = 100
    return order


# ---------- Discounts ----------
print("\n--- Discounts ---")
check("Default order has no discount (100)", make_order().calculate_total() == 100)
check("PercentageDiscount(10) gives 90",
      abs(make_order(PercentageDiscount(10)).calculate_total() - 90) < 0.001)
check("BulkDiscount(100, 20) gives 80 at the threshold",
      make_order(BulkDiscount(100, 20)).calculate_total() == 80)
check("BulkDiscount(200, 20) gives 100 below the threshold",
      make_order(BulkDiscount(200, 20)).calculate_total() == 100)
check("StudentDiscount() gives 85",
      abs(make_order(StudentDiscount()).calculate_total() - 85) < 0.001)

order = make_order()
before = order.calculate_total()
order.set_discount(PercentageDiscount(50))
check("set_discount() changes an existing order (100 -> 50)",
      before == 100 and abs(order.calculate_total() - 50) < 0.001)


class HalfPrice(DiscountStrategy):            # defined outside Order
    def apply(self, total):
        return total / 2


check("A new strategy works without changing Order",
      make_order(HalfPrice()).calculate_total() == 50)

order_source = inspect.getsource(Order)
check("Order contains no discount if/elif logic",
      not any(word in order_source for word in
              ("elif", "isinstance", "PercentageDiscount",
               "BulkDiscount", "StudentDiscount")))

# ---------- Factory ----------
print("\n--- Factory ---")
check("Factory creates a PhysicalProduct",
      isinstance(ProductFactory.create("Physical", "P1", "Mug", 5, 1,
                                       supplier, weight=1), PhysicalProduct))
check("Factory creates a DigitalProduct",
      isinstance(ProductFactory.create("Digital", "D1", "Ebook", 5, 1,
                                       supplier, download_size=2), DigitalProduct))
message = raises_value_error(ProductFactory.create, "service", "S1", "Install",
                             30.0, 5, supplier)
check("Unknown product type raises ValueError with a clear message",
      message is not None and "Unknown product type" in message)
print(f"      message was: {message}")

# ---------- Validation ----------
print("\n--- Validation ---")
check("Price of 0 is rejected",
      raises_value_error(ProductFactory.create, "Physical", "P1", "Mug", 0, 5,
                         supplier, weight=1) is not None)
check("Negative price is rejected",
      raises_value_error(ProductFactory.create, "Physical", "P1", "Mug", -5, 5,
                         supplier, weight=1) is not None)
check("Negative stock is rejected",
      raises_value_error(ProductFactory.create, "Physical", "P1", "Mug", 5, -1,
                         supplier, weight=1) is not None)
product = ProductFactory.create("Physical", "P1", "Mug", 5, 5, supplier, weight=1)
check("update_stock(-3) is rejected",
      raises_value_error(product.update_stock, -3) is not None)
check("Stock of 0 is allowed",
      raises_value_error(product.update_stock, 0) is None)
check("OrderLine quantity 0 is rejected",
      raises_value_error(OrderLine, product, 0) is not None)
check("OrderLine negative quantity is rejected",
      raises_value_error(OrderLine, product, -2) is not None)
empty_order = Order("O9")
raises_value_error(empty_order.add_order_line, product, 0)
check("A rejected quantity is not added to the order",
      len(empty_order.order_line) == 0)

# ---------- User input ----------
print("\n--- User input ---")
with patch("builtins.input", side_effect=["abc", "-3", "0", "12.5"]):
    with redirect_stdout(io.StringIO()) as out:
        value = get_positive_float("Price: ")
check("get_positive_float asks again until valid and returns 12.5", value == 12.5)
check("It showed a message for text input", "valid number" in out.getvalue())
check("It showed a message for zero/negative input",
      "greater than zero" in out.getvalue())

# ---------- CSV loading ----------
print("\n--- CSV loading ---")
CSV_TEXT = (
    "product_type,product_id,name,price,stock_quantity\n"
    "physical,P001,Desk Lamp,25.00,10\n"
    "digital,D001,Photo Editor,49.90,100\n"
    "service,S001,Installation,30.00,5\n"
    "physical,P002,Office Chair,abc,3\n"
    "physical,P003,Monitor Stand,39.50,7\n"
)

inventory = Inventory()
with redirect_stdout(io.StringIO()) as out:
    load_products("does_not_exist.csv", inventory, supplier)
text = out.getvalue()
check("Missing file: message printed, no crash", "not found" in text)
check("Missing file: finally block still runs", "Load attempt finished." in text)
check("Missing file: nothing loaded", len(inventory._products) == 0)

with tempfile.TemporaryDirectory() as folder:
    path = os.path.join(folder, "products.csv")
    with open(path, "w", newline="") as f:
        f.write(CSV_TEXT)
    inventory = Inventory()
    with redirect_stdout(io.StringIO()) as out:
        load_products(path, inventory, supplier)
text = out.getvalue()
ids = [p.get_product_id() for p in inventory._products]
check("Valid rows loaded (P001, D001, P003)", ids == ["P001", "D001", "P003"])
check("Unknown type row reported", "Unknown product type: 'service'" in text)
check("Non-numeric price row reported", "could not convert string to float" in text)
check("Count printed", "3 products loaded." in text)
check("finally message printed", "Load attempt finished." in text)

# ---------- Except clauses ----------
print("\n--- Except clauses ---")
for filename in ("inventory_manager.py", "inventory.py",
                 "product_factory.py", "order.py"):
    with open(os.path.join(PROJECT, filename)) as f:
        source = f.read()
    check(f"{filename}: no bare or broad except",
          "except:" not in source and "except Exception" not in source)

# ---------- Summary ----------
print(f"\n{passed} passed, {failed} failed")