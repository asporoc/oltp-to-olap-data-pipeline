from src.config import olap
from src.utils import get_connection
from fastapi import HTTPException
def get_runs():
    with get_connection(olap) as conn:
        curr = conn.cursor()

        curr.execute("""
            SELECT run_id, status, started_at, finished_at, triggered_by
            FROM metadata.pipeline_runs
            ORDER BY started_at DESC
        """)
        rows = curr.fetchall()
        columns = [desc[0] for desc in curr.description]
        result = [dict(zip(columns, row)) for row in rows]
        return result

def get_run_by_id(run_id):
    with get_connection(olap) as conn:
        curr = conn.cursor()

        curr.execute("""
        SELECT run_id, status, started_at, finished_at, triggered_by
        FROM metadata.pipeline_runs
        WHERE run_id = %s""",(run_id,))
        row = curr.fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="run not found")
        else:
            columns = [desc[0] for desc in curr.description]
            result = [dict(zip(columns, row))]
            return result