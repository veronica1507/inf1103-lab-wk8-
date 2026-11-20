from OrderLine import OrderLine
from product import Product
from discount import DiscountStrategy, NoDiscount


class Order():
    def __init__(self, order_id: str, discount_strategy: DiscountStrategy | None = None):
        self.order_id: str = order_id
        self.order_line: list[OrderLine] = []
        self._discount_strategy: DiscountStrategy = discount_strategy if discount_strategy is not None else NoDiscount()

    def set_discount(self, discount_strategy: DiscountStrategy) -> None:
        self._discount_strategy = discount_strategy

    def add_order_line(self, product: Product, quantity: int) -> None:
        order_line = OrderLine(product, quantity)
        self.order_line.append(order_line)

    def remove_order_line(self, order_line_obj) -> None:
        if order_line_obj in self.order_line:
            self.order_line.remove(order_line_obj)
            print("Order line removed successfully.")
        else:
            print("Order line not found in this order")

    def calculate_total(self) -> float:
        subtotal = 0
        for line in self.order_line:
            subtotal += line.calculate_subtotal()
        return self._discount_strategy.apply(subtotal)