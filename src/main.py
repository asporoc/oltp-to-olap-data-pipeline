from src.pipeline.extract.extract_addresses import extract_addresses
from src.pipeline.extract.extract_order_items import extract_order_items
from src.pipeline.extract.extract_orders import extract_orders
from src.pipeline.extract.extract_payments import extract_payments
from src.pipeline.extract.extract_products import extract_products
from src.config import olap

from pipeline.extract.extract_users import extract_users
from pipeline.metadata.run_logger import (
    start_pipeline_run,
    finish_pipeline_run,
    fail_pipeline_run
)
from src.pipeline.metadata.runs import get_runs, get_run_by_id
from src.pipeline.pipeline_run.run import run_pipeline
from src.utils import get_connection
if __name__ == "__main__":
    #run_pipeline()
    print(get_run_by_id(4))