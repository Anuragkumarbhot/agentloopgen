from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
import os

# -------------------------
# DATABASE CONFIG
# -------------------------

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

# -------------------------
# FASTAPI APP
# -------------------------

app = FastAPI(title="AgentLoopGen")

# -------------------------
# AGENT MODEL
# -------------------------

class Agent(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String)

    status = Column(String, default="active")

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


# -------------------------
# JOB MODEL
# -------------------------

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)

    agent_id = Column(Integer)

    task = Column(String)

    status = Column(
        String,
        default="pending"
    )

    attempts = Column(
        Integer,
        default=0
    )

    max_attempts = Column(
        Integer,
        default=3
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow
    )


# -------------------------
# ROOT
# -------------------------

@app.get("/")
def root():
    return {
        "status": "AgentLoopGen running",
        "phase": "Phase 4",
        "service": "backend"
    }


# -------------------------
# HEALTH CHECK
# -------------------------

@app.get("/health")
def health():
    return {
        "status": "ok"
    }


# -------------------------
# DATABASE HEALTH
# -------------------------

@app.get("/db-health")
def db_health():

    try:

        db = SessionLocal()

        db.execute("SELECT 1")

        db.close()

        return {
            "database": "connected",
            "status": "ok"
        }

    except Exception as e:

        return {
            "database": "error",
            "message": str(e)
        }


# -------------------------
# INIT AGENTS TABLE
# -------------------------

@app.get("/init-db")
def init_db():

    Base.metadata.create_all(bind=engine)

    return {
        "message": "agents table created"
    }


# -------------------------
# INIT JOBS TABLE
# -------------------------

@app.get("/init-jobs")
def init_jobs():

    Base.metadata.create_all(bind=engine)

    return {
        "message": "jobs table created"
    }


# -------------------------
# CREATE AGENT
# -------------------------

@app.post("/agents")
def create_agent(name: str):

    db = SessionLocal()

    agent = Agent(
        name=name,
        status="active"
    )

    db.add(agent)

    db.commit()

    db.refresh(agent)

    db.close()

    return {
        "id": agent.id,
        "name": agent.name,
        "status": agent.status
    }


# -------------------------
# GET AGENTS
# -------------------------

@app.get("/agents")
def get_agents():

    db = SessionLocal()

    agents = db.query(Agent).all()

    db.close()

    return agents


# -------------------------
# DELETE AGENT
# -------------------------

@app.delete("/agents/{agent_id}")
def delete_agent(agent_id: int):

    db = SessionLocal()

    agent = db.query(Agent).filter(
        Agent.id == agent_id
    ).first()

    if agent:

        db.delete(agent)

        db.commit()

        db.close()

        return {
            "message": "agent deleted"
        }

    db.close()

    return {
        "message": "agent not found"
    }


# -------------------------
# CREATE JOB
# -------------------------

@app.post("/jobs")
def create_job(
    agent_id: int,
    task: str
):

    db = SessionLocal()

    job = Job(
        agent_id=agent_id,
        task=task,
        status="pending"
    )

    db.add(job)

    db.commit()

    db.refresh(job)

    db.close()

    return {
        "id": job.id,
        "status": job.status
    }


# -------------------------
# GET JOBS
# -------------------------

@app.get("/jobs")
def get_jobs():

    db = SessionLocal()

    jobs = db.query(Job).all()

    db.close()

    return jobs


# -------------------------
# UPDATE JOB STATUS
# -------------------------

@app.put("/jobs/{job_id}")
def update_job_status(
    job_id: int,
    status: str
):

    db = SessionLocal()

    job = db.query(Job).filter(
        Job.id == job_id
    ).first()

    if job:

        job.status = status

        job.updated_at = datetime.utcnow()

        db.commit()

        db.close()

        return {
            "message": "job updated"
        }

    db.close()

    return {
        "message": "job not found"
    }
