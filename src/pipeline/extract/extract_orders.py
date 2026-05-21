from src.utils import get_connection
from src.config import oltp
from src.pipeline.metadata.run_logger import (
    start_pipeline_step,
    finish_pipeline_step,
    fail_pipeline_step
)

def extract_orders(run_id, olap_conn):
    step_id = None

    with get_connection(oltp) as oltp_conn:
        src_cur = oltp_conn.cursor()
        dst_cur = olap_conn.cursor()

        try:
            step_id = start_pipeline_step(
                dst_cur,
                run_id=run_id,
                step_name='extract_orders',
                table_name='raw.orders',
            )
            olap_conn.commit()

            dst_cur.execute("""
                SELECT COALESCE(MAX(pr.finished_at), TIMESTAMPTZ '1970-01-01 00:00:00+00')
                FROM metadata.pipeline_runs pr
                JOIN metadata.pipeline_steps ps
                  ON pr.run_id = ps.run_id
                WHERE pr.status = 'success'
                  AND ps.status = 'success'
                  AND ps.step_name = 'extract_orders'
            """)
            last_run = dst_cur.fetchone()[0]

            src_cur.execute("""
                SELECT *
                FROM orders
                WHERE updated_at > %s
            """, (last_run,))
            rows = src_cur.fetchall()

            rows_processed = 0
            for row in rows:
                dst_cur.execute("""
                    INSERT INTO raw.orders (
                        order_id,
                        user_id,
                        shipping_address_id,
                        billing_address_id,
                        order_status,
                        total_amount,
                        row_hash,
                        created_at,
                        updated_at,
                        is_deleted
                    )
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """, row)
                rows_processed += 1

            finish_pipeline_step(dst_cur, step_id, rows_processed)
            olap_conn.commit()

        except Exception as e:
            if step_id is not None:
                fail_pipeline_step(dst_cur, step_id, str(e))
                olap_conn.commit()
            raise