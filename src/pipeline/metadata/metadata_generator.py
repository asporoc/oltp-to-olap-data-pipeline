from src.utils import get_connection
from src.config import olap

with get_connection(olap) as conn:
    curr = conn.cursor()

def start_pipeline_run(cur, name, trigger, notes=None):
    cur.execute("""
        INSERT INTO metadata.pipeline_runs (
            pipeline_name,
            status,
            triggered_by,
            notes
        )
        VALUES (%s, %s, %s, %s)
        RETURNING run_id
    """, (name, 'running', trigger, notes))
    return cur.fetchone()[0]

def finish_pipeline_run(cur, run_id):
    cur.execute("""
        UPDATE metadata.pipeline_runs
        SET finished_at = NOW(),
            status = %s
        WHERE run_id = %s
    """, ('success', run_id))


def fail_pipeline_run(cur, run_id, notes=None):
    cur.execute("""
        UPDATE metadata.pipeline_runs
        SET finished_at = NOW(),
            status = %s,
            notes = %s
        WHERE run_id = %s
    """, ('failed', notes, run_id))

def start_pipeline_step(cur, run_id, step_name, table_name=None):
    cur.execute("""
        INSERT INTO metadata.pipeline_steps (
            run_id,
            step_name,
            table_name,
            status
        )
        VALUES (%s, %s, %s, %s)
        RETURNING step_id
    """, (run_id, step_name, table_name, 'running'))
    return cur.fetchone()[0]


def finish_pipeline_step(cur, step_id, rows_processed=0):
    cur.execute("""
        UPDATE metadata.pipeline_steps
        SET finished_at = NOW(),
            rows_processed = %s,
            status = %s
        WHERE step_id = %s
    """, (rows_processed, 'success', step_id))


def fail_pipeline_step(cur, step_id, error_message):
    cur.execute("""
        UPDATE metadata.pipeline_steps
        SET finished_at = NOW(),
            status = %s,
            error_message = %s
        WHERE step_id = %s
    """, ('failed', error_message, step_id))