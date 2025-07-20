from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client.products_db

# Only the admin should see unpublished products or internal flag

def get_product(product_id, user):
    product = db.products.find_one({'id': product_id}, {'_id': 0})
    if not product:
        return None
    # Enforce publication and authorization
    if not product.get('is_published', False):
        if not getattr(user, 'is_admin', False):
            return None
    # Remove internal debug fields unconditionally
    product.pop('internal_flag', None)
    return product

# Example usage
def current_user():
    # fetch from session or request context
    return {'username': 'alice', 'is_admin': False}

if __name__ == '__main__':
    user = current_user()
    prod = get_product(123, user)
    print(prod)
