import time
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import Job, DATABASE_URL


# -------------------------
# DATABASE CONNECTION
# -------------------------

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# -------------------------
# EXECUTION ENGINE
# -------------------------

def execute_task(task):

    print("Running task:", task)

    try:

        if task == "send_email":

            time.sleep(2)

            print("Email sent")

        elif task == "generate_report":

            time.sleep(3)

            print("Report generated")

        elif task == "process_data":

            time.sleep(2)

            print("Data processed")

        else:

            print("Unknown task")

        return True

    except Exception as e:

        print("Task error:", e)

        return False


# -------------------------
# PROCESS JOB
# -------------------------

def process_job(job, db):

    try:

        job.status = "running"

        job.attempts += 1

        job.updated_at = datetime.utcnow()

        db.commit()

        success = execute_task(job.task)

        if success:

            job.status = "completed"

        else:

            if job.attempts < job.max_attempts:

                job.status = "retrying"

            else:

                job.status = "failed"

        job.updated_at = datetime.utcnow()

        db.commit()

    except Exception as e:

        print("Process job error:", e)

        try:

            if job.attempts < job.max_attempts:

                job.status = "retrying"

            else:

                job.status = "failed"

            job.updated_at = datetime.utcnow()

            db.commit()

        except Exception as db_error:

            print("Database error:", db_error)


# -------------------------
# WORKER LOOP (SAFE)
# -------------------------

def worker():

    print("Worker started")

    while True:

        db = None

        try:

            db = SessionLocal()

            job = (
                db.query(Job)
                .filter(
                    Job.status.in_(["pending", "retrying"])
                )
                .order_by(Job.id)
                .first()
            )

            if job:

                print("Processing job:", job.id)

                process_job(job, db)

            else:

                print("No pending jobs")

        except Exception as e:

            print("Worker error:", e)

        finally:

            if db:

                db.close()

        time.sleep(5)


# -------------------------
# START WORKER
# -------------------------

if __name__ == "__main__":

    worker()
