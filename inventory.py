from product import Product , PhysicalProduct , DigitalProduct
from supplier import Supplier
from product_factory import ProductFactory

class Inventory:
    def __init__(self):
        self._products: list[Product] = []

    def add_product(self, product: Product) -> bool:
        if self.find_product(product.get_product_id()) is not None:
            print("Product ID already exists.")
            return False
        self._products.append(product)
        return True

    def remove_product(self,product_id):
        p: Product | None = self.find_product(product_id)
        if p is None:
            print("Product ID does not exist.")
        self._products.remove(p)
        
    def display_all (self):
        print("Current Inventory")
        print("-"*50)
        if not self._products:
            print("There are no items in the inventory")
            return
        for product in self._products:
            self.show_product_details(product)
            print("-"*28)

    def show_product_details(self, product: Product):
        product.display_information()
        print(product.get_fulfilment_info())
        product.supplier.display_information()

    def find_product(self,id: str) -> Product | None:
        for product in self._products:
            if product.get_product_id() == id:
                print ("Item Found")
                product.display_information()
                return product

    def load_products(self, products: list[dict[str, str | float | int]], suppliers: list[Supplier]):
        common_keys = {"product_id", "name", "price", "stock", "supplier", "type"}
        for item in products:
            supplier = None
            for s in suppliers:
                if s.supplier_id == item["supplier"]:
                    supplier = s
                    break

            if supplier is None:
                print(f"Supplier with ID {item['supplier']} not found.")
                continue

            extra = {k: v for k, v in item.items() if k not in common_keys}
            try:
                product = ProductFactory.create(
                    item.get("type"), item["product_id"], item["name"],
                    item["price"], item["stock"], supplier, **extra
            )
            except (ValueError, TypeError) as e:
                print(f"Skipping product {item.get('product_id')}: {e}")
                continue
            self.add_product(product)

    def get_all_products_dict(self) -> dict[str,list[dict[str, str | float | int]]]:
        products: list[dict[str,str | float | int]] = []
        for product in self._products:
            products.append(product.to_dict())
        return {"products": products}

