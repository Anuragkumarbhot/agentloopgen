import time
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import Job, DATABASE_URL

# -------------------------
# DATABASE
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

    print(f"Running task: {task}")

    # Example tasks
    if task == "send_email":

        time.sleep(2)

        print("Email sent")

        return True

    elif task == "generate_report":

        time.sleep(3)

        print("Report generated")

        return True

    elif task == "process_data":

        time.sleep(2)

        print("Data processed")

        return True

    else:

        print("Unknown task")

        return True


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

        print("Error:", e)

        if job.attempts < job.max_attempts:

            job.status = "retrying"

        else:

            job.status = "failed"

        job.updated_at = datetime.utcnow()

        db.commit()


# -------------------------
# WORKER LOOP
# -------------------------

def worker():

    print("Worker started")

    while True:

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

            print(f"Processing job {job.id}")

            process_job(job, db)

        db.close()

        time.sleep(5)


if __name__ == "__main__":

    worker()
