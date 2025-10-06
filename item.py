class Item :
    name : str
    company : str
    price_to_weight : str
    image_link : str
    product_type : str
    price : float

    def __init__(self, na : str = "", co : str = "", pw : str = "", li : str = "", pt : str = "",  pr : float = 0.00):
        self.name = na
        self.company = co
        self.price = pr
        self.price_to_weight = pw
        self.product_type = pt
        self.image_link = li
    
    def __str__(self):
        return f"Item [\n   Nom : {self.name}\n   Type de produit : {self.product_type}\n   Compagnie : {self.company}\n   Prix : {self.price}\n   Prix par poid : {self.price_to_weight}\n   Lien image : {self.image_link}\n]"