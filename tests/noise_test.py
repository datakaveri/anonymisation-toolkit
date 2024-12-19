import pytest
import pandas as pd

from src.cdpg_anonkit.noise import DifferentialPrivacy

@pytest.fixture
def base_results():
    return pd.DataFrame({
        'H3': ['abc', 'def', 'ghi'],
        'date': ['2023-01-01', '2023-01-02', '2023-01-03'],
        'count': [10, 15, 20]
    })

def test_differential_privacy_laplace_mechanism():
    """
    Test the Laplace mechanism of DifferentialPrivacy class.
    """
    dp = DifferentialPrivacy(mechanism='laplace', epsilon=1.0)
    original_value = 10
    sensitivity = 1.0
    noisy_value = dp.add_noise(original_value, sensitivity)
    
    # Check that the noisy value is a float and different from the original value
    assert isinstance(noisy_value, float)
    assert noisy_value != original_value

def test_differential_privacy_clip_count():
    """
    Test the clip_count method of DifferentialPrivacy class.
    """
    clipped_value = DifferentialPrivacy.clip_count(15, lower_bound=0, upper_bound=10)
    assert clipped_value == 10
    
    clipped_value = DifferentialPrivacy.clip_count(-5, lower_bound=0)
    assert clipped_value == 0

def test_differential_privacy_compute_sensitivity():
    """
    Test the compute_sensitivity method of DifferentialPrivacy class.
    """
    dp = DifferentialPrivacy(mechanism='laplace', epsilon=1.0)
    sensitivity = dp.compute_sensitivity('count')
    assert sensitivity == 1.0

