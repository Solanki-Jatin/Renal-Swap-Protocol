"""
FastAPI entrypoint. This is deliberately a thin layer over the
algorithm core, every endpoint here just calls functions that already
exist and are already tested inside algorithm_core, nothing new gets
decided at this layer. That separation is what lets the algorithm
core be demoed and verified with zero web framework involved.

Run with:
    uvicorn api.main:app --reload

Interactive docs will then be available at:
    http://localhost:8000/docs
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import benchmark, dataset, graph, match

app = FastAPI(
    title="Renal Swap Exchange API",
    description=(
        "Kidney exchange matching, backed by real cycle detection "
        "and integer programming, not a language model."
    ),
    version="0.1.0",
)

# The frontend runs on a different port during development (Vite's
# default is 5173), so CORS needs to stay open for it to reach this
# API at all. Fine for a hackathon demo, would need tightening for
# any real deployment.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dataset.router)
app.include_router(graph.router)
app.include_router(match.router)
app.include_router(benchmark.router)


@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "Renal Swap Exchange API is running. See /docs for available endpoints.",
    }
