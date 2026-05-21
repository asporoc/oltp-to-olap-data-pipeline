from src.config import olap
from src.pipeline.extract.extract_addresses import extract_addresses
from src.pipeline.extract.extract_order_items import extract_order_items
from src.pipeline.extract.extract_orders import extract_orders
from src.pipeline.extract.extract_payments import extract_payments
from src.pipeline.extract.extract_products import extract_products
from src.pipeline.extract.extract_users import extract_users
from src.pipeline.metadata.run_logger import start_pipeline_run, finish_pipeline_run, fail_pipeline_run
from src.utils import get_connection


def run_pipeline():
    run_id = None

    with get_connection(olap) as olap_conn:
        cur = olap_conn.cursor()

        try:
            run_id = start_pipeline_run(
                cur,
                name='oltp_to_olap',
                trigger='manual',
                notes='api run'
            )
            olap_conn.commit()

            extract_users(run_id, olap_conn)
            extract_addresses(run_id, olap_conn)
            extract_orders(run_id, olap_conn)
            extract_order_items(run_id, olap_conn)
            extract_payments(run_id, olap_conn)
            extract_products(run_id, olap_conn)

            finish_pipeline_run(cur, run_id)
            olap_conn.commit()

            return {"run_id": run_id, "status": "success"}

        except Exception as e:
            if run_id is not None:
                fail_pipeline_run(cur, run_id, str(e))
                olap_conn.commit()
            raise