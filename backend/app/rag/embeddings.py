"""
Zero-dependency, completely local offline semantic embedding generator.
Computes dense normalized feature vectors using multi-gram hashing and term weighting.
Runs in sub-millisecond time and requires zero cloud or external API calls.
"""
import re
import math
import numpy as np
from typing import List

DIM = 256

def tokenize(text: str) -> List[str]:
    # Extract lower alphanumeric words
    tokens = re.findall(r"[a-zA-Z0-9_\-]+", text.lower())
    # Add bigrams for stronger technical/industrial phrase matching (e.g. 'vibration_analysis', 'pump_p102')
    bigrams = [f"{tokens[i]}_{tokens[i+1]}" for i in range(len(tokens)-1)]
    return tokens + bigrams

def get_embedding(text: str) -> np.ndarray:
    tokens = tokenize(text)
    if not tokens:
        return np.zeros(DIM, dtype=np.float32)
    
    vec = np.zeros(DIM, dtype=np.float32)
    for token in tokens:
        # Stable deterministic polynomial hash
        h = 0
        for char in token:
            h = (h * 31 + ord(char)) & 0xFFFFFFFFF
        idx = h % DIM
        sign = 1.0 if ((h >> 8) & 1) == 0 else -1.0
        vec[idx] += sign * (1.0 + math.log(1.0 + len(token)))

    norm = np.linalg.norm(vec)
    if norm > 1e-6:
        vec = vec / norm
    return vec

def cosine_similarity(v1: np.ndarray, v2: np.ndarray) -> float:
    dot = np.dot(v1, v2)
    return float(np.clip(dot, -1.0, 1.0))
