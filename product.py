from abc import ABC, abstractmethod

class CanBeShipped(ABC):
    @abstractmethod
    def calculate_shipping_cost():
        pass


class Product(ABC):
    @abstractmethod
    def __init__(self,product_id,name,price,stock):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock

    def update_stock(self,quantity):
        self.__stock = quantity

    def get_product_id(self):
        return self.__product_id

    def display_information(self):
        print (f" Product ID: {self.__product_id} \n Product Name: {self.__name} \n Price: {self.__price} \n Stock: {self.__stock}")

    def get_fulfilment_info():
        pass
    
    
    def to_dict(self):
        return {
            "product_id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock
        }

class PhysicalProduct(Product):
    def __init__(self,product_id,name,price,stock,weight):
        super().__init__(product_id, name,price,stock)
        self.__weight = weight

    def display_information(self):
        super().display_information()
        print(f"Weight: {self.__weight}kg")

    def to_dict(self):
            product = super().to_dict()
            product["weight"] = self.__weight
            return product

class DigitalProduct(Product):
    def __init__(self,product_id,name,price,stock,download_size):
        super().__init__(product_id, name,price,stock)
        self.__download_size = download_size

    def display_information(self):
        super().display_information()
        print(f"Downloadable Size: {self.__download_size}MB")
   
    def to_dict(self):
        product = super().to_dict()
        product["download_size"] = self.__download_size
        return product