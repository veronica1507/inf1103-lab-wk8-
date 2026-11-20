from abc import ABC, abstractmethod
from supplier import Supplier

class CanBeShipped(ABC):
    @abstractmethod
    def calculate_shipping_cost():
        pass


class Product(ABC):
    def __init__(self,product_id: str,name: str,price: float,stock: int, supplier: Supplier):
        self._product_id = product_id
        self._name = name
        self._price = price
        self._stock = 0
        self.update_stock(stock)
        self._supplier: Supplier = supplier

    def update_stock(self,quantity):
        if quantity < 0:
            raise ValueError("Stock quantity cannot be negative.")
        self._stock = quantity

    def get_product_id(self):
        return self._product_id

    def display_information(self):
        print (f" Product ID: {self._product_id} \n Product Name: {self._name} \n Price: {self._price} \n Stock: {self._stock}")

    @property
    def supplier(self):
        return self._supplier

    @abstractmethod
    def get_fulfilment_info(self):
        pass
    
    def to_dict(self):
        return {
            "product_id": self._product_id,
            "name": self._name,
            "price": self._price,
            "stock": self._stock,
            "supplier": self._supplier.supplier_id
        }

class PhysicalProduct(Product,CanBeShipped):
    def __init__(self,product_id: str,name: str,price: float,stock: int,supplier: Supplier,weight: float=1.0):
        super().__init__(product_id, name,price,stock,supplier)
        self._weight = weight

    def display_information(self):
        super().display_information()
        print(f"Weight: {self._weight}kg")
        self._supplier.display_information()

    def to_dict(self):
            product = super().to_dict()
            product["type"] = "Physical"
            product["weight"] = self._weight
            return product

    def get_fulfilment_info(self):
        print("The product requires shipping.")

    def calculate_shipping_cost(self):
        return 1.5 * self._weight

class DigitalProduct(Product):
    def __init__(self,product_id: str,name: str,price: float,stock: int,supplier: Supplier,download_size: float=1.0):
        super().__init__(product_id, name,price,stock,supplier)
        self._download_size = download_size

    def display_information(self):
        super().display_information()
        print(f"Downloadable Size: {self._download_size}MB")
        self._supplier.display_information()
   
    def to_dict(self):
        product = super().to_dict()
        product["type"] = "Digital"
        product["download_size"] = self._download_size
        return product

    def get_fulfilment_info(self):
        print("The product is delivered digitally")