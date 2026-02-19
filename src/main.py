from src.generators import genUsers
from src.ingestion.db_ingest import insert_user

for user in genUsers(3):
    insert_user(user)
