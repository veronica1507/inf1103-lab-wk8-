from product import Product

class Inventory:
    def __init__(self):
        self.__products =[]

    def add_product(self,product_id,name,price,stock):
        new_product = Product(product_id,name,price,stock)
        self.__products.append(new_product)
        print(f"Added {name} to inventory !")

    def display_all (self):
        for product in self.__products:
            product.display_information()
            print("-"*28)
