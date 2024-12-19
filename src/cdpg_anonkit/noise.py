import numpy as np
import pandas as pd
from typing import Union, Optional, Dict, Any, Callable, Literal

class DifferentialPrivacy:
    """
    Differential Privacy mechanism with support for various noise addition strategies.
    
    Focuses on fundamental DP principles with extensibility in mind.
    """
    
    def __init__(self, 
                 mechanism: Literal['laplace', 'gaussian', 'exponential'], 
                 epsilon: float = 1.0, 
                 delta: Optional[float] = None,
                 sensitivity: Optional[float] = None):

        """
        Initialises a DifferentialPrivacy object with specified parameters.

        Parameters
        ----------
        mechanism : Literal['laplace', 'gaussian', 'exponential']
            The differential privacy mechanism to use
        epsilon : float, optional
            The privacy budget for the mechanism, by default 1.0
        delta : Optional[float], optional
            The probability of a failure of the mechanism, by default None
        sensitivity : Optional[float], optional
            The sensitivity of the query, by default None

        Raises
        ------
        ValueError
            If epsilon is not between 0 and 10
            If mechanism is not one of 'laplace', 'gaussian', 'exponential'
        """
        if not (0 < epsilon <= 10):
            raise ValueError("Epsilon must be between 0 and 10")
        
        self.mechanism = mechanism.lower()
        self.epsilon = epsilon
        self.delta = delta
        self._sensitivity = sensitivity
        
        # Validate mechanism
        if mechanism not in ['laplace', 'gaussian', 'exponential']:
            raise ValueError(f"Unsupported mechanism: {mechanism}")
    
    @staticmethod
    def clip_count(count: int, 
                   lower_bound: int = 0, 
                   upper_bound: Optional[int] = None) -> int:

        """
        Clip the count to a specified range.

        This static method ensures that the count provided falls within the 
        specified lower and upper bounds. If the upper bound is not provided, 
        the count is clipped to the lower bound only.

        Parameters
        ----------
        count : int
            The original count to be clipped.
        lower_bound : int, optional
            The minimum value to clip to, by default 0.
        upper_bound : Optional[int], optional
            The maximum value to clip to, by default None.

        Returns
        -------
        int
            The clipped count, constrained by the specified bounds.
        """

        if upper_bound is None:
            return max(lower_bound, count)
        
        return max(lower_bound, min(count, upper_bound))
    
    def compute_sensitivity(self, 
                            query_type: str = 'count', 
                            lower_bound: int = 0, 
                            upper_bound: Optional[int] = None) -> float:

        """
        Compute the sensitivity of a query based on its type and bounds.

        Sensitivity is a measure of how much the output of a query can change by 
        modifying a single record in the dataset. It is crucial for determining 
        the amount of noise to add in differential privacy mechanisms.

        Parameters
        ----------
        query_type : str, optional
            The type of query for which sensitivity is being computed. 
            Currently supported: 'count'. Defaults to 'count'.
        lower_bound : int, optional
            The minimum value constraint for the query. Defaults to 0.
        upper_bound : Optional[int], optional
            The maximum value constraint for the query. If None, no upper 
            bound is considered. Defaults to None.

        Returns
        -------
        float
            The sensitivity of the query. For 'count' queries, this is 1.0.

        Raises
        ------
        ValueError
            If the sensitivity computation for the specified query_type is 
            not implemented.
        """

        if query_type == 'count':
            # Sensitivity for count is 1 by definition
            # This represents the maximum change possible by adding/removing one record
            return 1.0
        
        raise ValueError(f"Sensitivity computation not implemented for {query_type}")
    
    def add_noise(self, 
                  value: Union[int, float], 
                  sensitivity: Optional[float] = None,
                  epsilon: Optional[float] = None) -> Union[int, float]:
        
        """
        Add noise to a given value according to the specified differential privacy mechanism.

        Depending on the mechanism set during initialization, this method will add
        noise to the input value to ensure differential privacy. Currently, the Laplace
        mechanism is implemented, with plans to support Gaussian and Exponential mechanisms.

        Parameters
        ----------
        value : Union[int, float]
            The original value to which noise will be added.
        sensitivity : Optional[float], optional
            The sensitivity of the query. If not provided, the class-level sensitivity
            will be used. Defaults to None.
        epsilon : Optional[float], optional
            The privacy budget. If not provided, the class-level epsilon will be used.
            Defaults to None.

        Returns
        -------
        Union[int, float]
            The value with added noise according to the specified mechanism.

        Raises
        ------
        ValueError
            If the Gaussian mechanism is selected but delta is not specified.
            If the mechanism is unsupported.
        NotImplementedError
            If the Gaussian or Exponential mechanism is selected, as they are not yet implemented.
        """
        # Use class-level sensitivity if not provided
        sensitivity = sensitivity or self._sensitivity or 1.0
        
        # Use class-level epsilon if not provided
        epsilon = epsilon or self.epsilon
        
        if self.mechanism == 'laplace':
            # Laplace mechanism: Noise drawn from Laplace distribution
            # Noise scale is sensitivity / epsilon
            noise = np.random.laplace(0, sensitivity / epsilon)
            return value + noise
        
        elif self.mechanism == 'gaussian':
            # Gaussian mechanism
            # Requires delta parameter
            if self.delta is None:
                raise ValueError("Delta must be specified for Gaussian mechanism")
            raise NotImplementedError("Gaussian mechanism not yet implemented")
        #     # Noise scale computation following the Gaussian mechanism
        #     noise_scale = np.sqrt(2 * np.log(1.25 / self.delta)) * (sensitivity / epsilon)
        #     noise = np.random.normal(0, noise_scale)
        #     return value + noise
        
        elif self.mechanism == 'exponential':
            # Exponential mechanism
            # Requires a utility function and sensitivity
            raise NotImplementedError("Exponential mechanism not yet implemented")
        
        else:
            raise ValueError(f"Unsupported mechanism: {self.mechanism}")

def example_differential_privacy_usage():
    """
    Demonstrate usage of Differential Privacy with count query.
    
    Assumes IncrementalGroupbyAggregator has been used to compute base counts.
    """
    # Simulated base results from IncrementalGroupbyAggregator
    base_results = pd.DataFrame({
        'H3': ['abc', 'def', 'ghi'],
        'date': ['2023-01-01', '2023-01-02', '2023-01-03'],
        'count': [10, 15, 20]
    })
    
    # Different DP mechanism scenarios
    scenarios = [
        {
            'mechanism': 'laplace', 
            'epsilon': 1.0,
            'description': 'Laplace Mechanism with ε=1.0'
        },
        # {
        #     'mechanism': 'gaussian', 
        #     'epsilon': 1.0, 
        #     'delta': 1e-5,
        #     'description': 'Gaussian Mechanism with ε=1.0, δ=1e-5'
        # }
    ]
    
    for scenario in scenarios:
        print(f"\n{scenario['description']}")
        
        # Initialize Differential Privacy
        dp = DifferentialPrivacy(
            mechanism=scenario['mechanism'], 
            epsilon=scenario['epsilon'],
            delta=scenario.get('delta')
        )
        
        # Process each row
        noisy_results = []
        for _, row in base_results.iterrows():
            # Compute sensitivity
            sensitivity = dp.compute_sensitivity('count')
            
            # Clip count to ensure reasonable bounds
            clipped_count = dp.clip_count(row['count'], lower_bound=0)
            
            # Add noise to count
            noisy_count = dp.add_noise(clipped_count, sensitivity)
            
            noisy_results.append({
                'H3': row['H3'],
                'date': row['date'],
                'original_count': row['count'],
                'noisy_count': noisy_count
            })
        
        # Display results
        print(pd.DataFrame(noisy_results))

# Uncomment to run example
# example_differential_privacy_usage()