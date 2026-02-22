from src.generators import genUsers, genProducts
from src.ingestion.db_ingest import insert_user, insert_product

#for user in genUsers(3):
#    insert_user(user)
for product in genProducts(3):
    insert_product(product)
