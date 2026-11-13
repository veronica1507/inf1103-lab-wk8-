from product import Product , PhysicalProduct , DigitalProduct
from supplier import Supplier

class Inventory:
    def __init__(self):
        self._products: list[Product] = []

    def add_product(self, product: Product) -> None:
        p: Product | None = self.find_product(Product.id)
        if p is not None:
            print("Product ID already exists.")
        self._products.append(product)

    def remove_product(self,product_id):
        p: Product | None = self.find_product(product_id)
        if p is None:
            print("Product ID does not exist.")
        self._products.remove(p)
        
    def display_all (self):
        for product in self._products:
            product.display_information()
            product.get_fulfilment_info()
            print("-"*28)

    def find_product(self,id: str) -> Product | None:
        for product in self._products:
            if product.get_product_id() == id:
                print ("Item Found")
                product.display_information()
                return product
        return None

    def load_products(self,products: list[dict[str,str | float | int]], suppliers: list[Supplier]):
        for item in products:
            supplier = None
            for s in suppliers:
                if s.supplier_id == item["supplier"]:
                    supplier = s
                    break
                if supplier is None:
                    print(f"Supplier with ID {item['supplier']} not found.")
                product_type = item.get("type")
                if product_type == "Physical":
                    self.add_product(PhysicalProduct(item["product_id"], item["name"], item["price"], item["stock"], item["weight"]))

                elif product_type == "Digital":
                    self.add_product(DigitalProduct(item["product_id"], item["name"], item["price"], item["stock"], item["download_size"]))

    def get_all_products_dict(self) -> dict[str,list[dict[str, str | float | int]]]:
        products: list[dict[str,str | float | int]] = []
        for product in self._products:
            products.append(product.to_dict())
        return {"products": products}

