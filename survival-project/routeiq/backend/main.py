
from fastapi import FastAPI
import os
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI(title="AgentLoopGen")

DATABASE_URL = os.environ.get("DATABASE_URL")


def get_connection():
    return psycopg2.connect(DATABASE_URL)


# -------------------
# Basic routes
# -------------------

@app.get("/")
def root():
    return {
        "status": "AgentLoopGen running",
        "phase": "Phase 4",
        "service": "backend"
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/info")
def info():
    return {
        "app": "AgentLoopGen",
        "version": "1.0"
    }


@app.get("/db-health")
def db_health():
    try:
        conn = get_connection()
        conn.close()

        return {
            "database": "connected",
            "status": "ok"
        }

    except Exception as e:
        return {
            "database": "error",
            "details": str(e)
        }


# -------------------
# Initialize Agents table
# -------------------

@app.get("/init-db")
def init_db():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS agents (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            status TEXT DEFAULT 'active'
        )
    """)

    conn.commit()

    cur.close()
    conn.close()

    return {
        "message": "agents table created"
    }


# -------------------
# Initialize Jobs table
# -------------------

@app.get("/init-jobs")
def init_jobs():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id SERIAL PRIMARY KEY,
            task TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            retries INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()

    cur.close()
    conn.close()

    return {
        "message": "jobs table created"
    }


# -------------------
# Agents APIs
# -------------------

@app.post("/agents")
def create_agent(name: str):

    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute(
        "INSERT INTO agents (name) VALUES (%s) RETURNING *",
        (name,)
    )

    agent = cur.fetchone()

    conn.commit()

    cur.close()
    conn.close()

    return agent


@app.get("/agents")
def get_agents():

    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("SELECT * FROM agents")

    agents = cur.fetchall()

    cur.close()
    conn.close()

    return agents


@app.delete("/agents/{agent_id}")
def delete_agent(agent_id: int):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM agents WHERE id = %s",
        (agent_id,)
    )

    conn.commit()

    cur.close()
    conn.close()

    return {
        "message": "agent deleted"
    }


# -------------------
# Jobs APIs
# -------------------

@app.post("/jobs")
def create_job(task: str):

    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute(
        "INSERT INTO jobs (task) VALUES (%s) RETURNING *",
        (task,)
    )

    job = cur.fetchone()

    conn.commit()

    cur.close()
    conn.close()

    return job


@app.get("/jobs")
def get_jobs():

    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute(
        "SELECT * FROM jobs ORDER BY id DESC"
    )

    jobs = cur.fetchall()

    cur.close()
    conn.close()

    return jobs


@app.delete("/jobs/{job_id}")
def delete_job(job_id: int):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM jobs WHERE id = %s",
        (job_id,)
    )

    conn.commit()

    cur.close()
    conn.close()

    return {
        "message": "job deleted"
    }
