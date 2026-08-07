from typing import List, Optional

from pydantic import BaseModel, Field

from .pair import PairOut


class GenerateDatasetRequest(BaseModel):
    """
    Shared request shape for every endpoint that needs a pool of pairs
    to work with. dataset/generate uses it directly, graph/build and
    match/optimal and match/greedy all accept the same shape, since
    each of them starts by generating a pool before doing its own work.
    """
    count: int = Field(default=30, gt=0, le=5000, description="How many incompatible pairs to generate")
    hospital_ids: Optional[List[str]] = Field(
        default=None, description="Simulates a multi hospital pool, defaults to a single hospital"
    )
    seed: Optional[int] = Field(default=None, description="Set this for a reproducible dataset")


class GenerateDatasetResponse(BaseModel):
    pairs: List[PairOut]
    total: int
