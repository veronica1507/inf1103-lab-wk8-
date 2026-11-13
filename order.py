from OrderLine import OrderLine
from product import Product, PhysicalProduct, DigitalProduct
from supplier import Supplier

class Order():
    def __init__(self, order_id: str):
        self.order_id: str = order_id
        self.order_line: list[OrderLine] = []

    def add_order_line (self, product: Product, quantity: int) -> None:
        order_line = OrderLine(product, quantity)
        self.order_line.append(order_line)

    def remove_order_line(self, order_line_obj)-> None:
        if order_line_obj in self.order_line:
            self.order_line.remove(order_line_obj)
            print("Order line removed successfully.")
        else:
            print("Order line not found in this order")

    def calculate_total(self):
        sum = 0
        for i in self.order_line:
            cost = i.calculate_subtotal()
            sum = sum + cost
        return sum
