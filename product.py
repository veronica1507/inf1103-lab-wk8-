class Product:
    def __init__(self,product_id,name,price,stock):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock

    def update_stock(self,quantity):
        self.__stock = quantity

    def display_information(self):
        print (f" Product ID: {self.__product_id} \n Product Name: {self.__name} \n Price: {self.__price} \n Stock: {self.__stock}")
