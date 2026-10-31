from product import Product , PhysicalProduct , DigitalProduct

class Inventory:
    def __init__(self):
        self.__products =[]

    def add_product(self,product_obj):
        self.__products.append(product_obj)
        
    def display_all (self):
        for product in self.__products:
            product.display_information()
            product.get_fulfilment_info()
            print("-"*28)

    def search_product(self,id):
        for product in self.__products:
            if product.get_product_id() == id:
                print ("Item Found")
                product.display_information()
                return product
        print(f"Product with ID {id} not found.")

    def load_products(self,products):
        for item in products:
            if item["type"] == "Physical":
                self.add_product(PhysicalProduct(item["product_id"], item["name"], item["price"], item["stock"], item["weight"]))

            elif item["type"] == "Digital":
                self.add_product(DigitalProduct(item["product_id"], item["name"], item["price"], item["stock"], item["download_size"]))

    def get_all_products_dict(self):
        product_list = []
        for product in self.__products:
            product_list.append(product.to_dict())
        return product_list