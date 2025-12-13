"""Parameter optimization for strategies."""
import random
from typing import Dict, List, Callable
import numpy as np


class ParameterOptimizer:
    """Optimize strategy parameters using simple algorithms."""
    
    def __init__(self, param_space: Dict[str, tuple]):
        self.param_space = param_space  # {param_name: (min, max, step)}
        self.best_params = None
        self.best_score = float('-inf')
        self.history = []

    def random_search(self, objective_fn: Callable, iterations: int = 100) -> Dict:
        """Random parameter search."""
        for _ in range(iterations):
            params = {}
            for param_name, (min_val, max_val, step) in self.param_space.items():
                params[param_name] = random.uniform(min_val, max_val)
            
            score = objective_fn(params)
            self.history.append((params, score))
            
            if score > self.best_score:
                self.best_score = score
                self.best_params = params
        
        return self.best_params

    def grid_search(self, objective_fn: Callable) -> Dict:
        """Exhaustive grid search (for small parameter spaces)."""
        param_names = list(self.param_space.keys())
        ranges = [
            np.arange(min_v, max_v, step)
            for min_v, max_v, step in self.param_space.values()
        ]
        
        best_score = float('-inf')
        best_params = None
        
        for combo in np.ndindex(tuple(len(r) for r in ranges)):
            params = {name: ranges[i][combo[i]] for i, name in enumerate(param_names)}
            score = objective_fn(params)
            
            if score > best_score:
                best_score = score
                best_params = params
        
        self.best_params = best_params
        self.best_score = best_score
        return best_params
