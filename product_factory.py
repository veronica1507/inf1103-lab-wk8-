from product import Product, PhysicalProduct, DigitalProduct
from supplier import Supplier


class ProductFactory:
    # Maps the type string to the class that builds it.
    _product_types: dict[str, type[Product]] = {
        "Physical": PhysicalProduct,
        "Digital": DigitalProduct,
    }

    @staticmethod
    def create(product_type: str, product_id: str, name: str, price: float,
               stock: int, supplier: Supplier, **extra) -> Product:
        """
        extra holds the type-specific value:
          Physical -> weight=<float>
          Digital  -> download_size=<float>
        """
        product_class = ProductFactory._product_types.get(product_type.strip().capitalize())
        if product_class is None:
            raise ValueError(f"Unknown product type: '{product_type}'")
        return product_class(product_id, name, price, stock, supplier, **extra)