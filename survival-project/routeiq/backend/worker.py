import os
import time
import psycopg2

DATABASE_URL = os.environ.get("DATABASE_URL")


def get_connection():
    return psycopg2.connect(DATABASE_URL)


def process_job(job_id, task):

    print(f"Processing job {job_id}: {task}")

    time.sleep(5)

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "UPDATE jobs SET status = 'completed' WHERE id = %s",
        (job_id,)
    )

    conn.commit()

    cur.close()
    conn.close()


def worker_loop():

    while True:

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, task
            FROM jobs
            WHERE status = 'pending'
            ORDER BY id
            LIMIT 1
        """)

        job = cur.fetchone()

        if job:

            job_id, task = job

            cur.execute(
                "UPDATE jobs SET status = 'running' WHERE id = %s",
                (job_id,)
            )

            conn.commit()

            cur.close()
            conn.close()

            process_job(job_id, task)

        else:

            cur.close()
            conn.close()

            time.sleep(3)


if __name__ == "__main__":
    worker_loop()
