from dataclasses import dataclass
import numpy as np
from numpy.typing import NDArray


@dataclass
class DocumentEmbedding:
    document_id: str
    vector: NDArray[np.float32]
    model_version: str
    created_at: float
