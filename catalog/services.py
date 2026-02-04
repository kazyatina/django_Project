from catalog.models import Product

def get_list_products(category_id):
    return Product.objects.filter(category=category_id)

