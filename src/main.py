from src.generators import genUsers, genProducts, genOrders
from src.ingestion.db_ingest import insert_user, insert_product, insert_order

#for user in genUsers(3):
#    insert_user(user)
#for product in genProducts(3):
#    insert_product(product)

for u in genOrders(3):
    insert_order(u)