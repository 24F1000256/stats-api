import time
import uuid

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

ALLOWED_ORIGIN = "https://dash-zduxnr.example.com"
EMAIL = "24f1000256@ds.study.iitm.ac.in"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID", "X-Process-Time"],
)


@app.middleware("http")
async def add_headers(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    response.headers["X-Request-ID"] = str(uuid.uuid4())
    response.headers["X-Process-Time"] = f"{time.perf_counter() - start:.6f}"
    return response


@app.get("/")
def root():
    return {"status": "ok"}


@app.get("/stats")
def stats(values: str = ""):
    try:
        nums = [int(v.strip()) for v in values.split(",") if v.strip() != ""]
    except ValueError:
        raise HTTPException(status_code=400, detail="values must be comma-separated integers")
    if not nums:
        raise HTTPException(status_code=400, detail="no values provided")
    total = sum(nums)
    return {
        "email": EMAIL,
        "count": len(nums),
        "sum": total,
        "min": min(nums),
        "max": max(nums),
        "mean": total / len(nums),
    }
@app.get("/q13")
def q13():
    return {
        "A": {"text": "Report job-5264c509: caf\u00e9\nReady \u2713", "complete": True, "error": None},
        "B": {"text": "Partial job-5264c509", "complete": False, "error": None},
        "C": {"text": "Draft job-5264c509", "complete": False, "error": "model unloaded"},
    }


@app.get("/q14")
def q14():
    return {
        "A": {"steps": ["L3", "L4", "L5"], "seconds": 41},
        "B": {"steps": ["L1", "L2", "L3", "L4", "L5"], "seconds": 109},
        "C": {"steps": [], "seconds": 0},
        "D": {"steps": [], "seconds": 0},
        "E": {"steps": ["L4", "L5"], "seconds": 41},
    }