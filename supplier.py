class Supplier:
    def __init__(self,supplier_id: str,name: str,contact_email: str):
        self._supplier_id: str = supplier_id
        self._name: str = name
        self._contact_email: str = contact_email

    def display_information(self):
        print (f"Supplier ID: {self._supplier_id} \n Supplier Name: {self._name} \n Contact Email: {self._contact_email}")