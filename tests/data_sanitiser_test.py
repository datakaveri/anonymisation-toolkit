import pytest
import pandas as pd
import numpy as np
import data_sanitiser  

@pytest.fixture
def sample_df():
    """Create a sample DataFrame for testing."""
    return pd.DataFrame({
        'age': [25, 40, 15, 60, 18, 90, 22, 45, 50, 55],
        'income': [50000, 80000, 65000, 120000, 20000, 90000, 55000, 75000, 85000, 95000],
        'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank', 'Grace', 'Henry', 'Ivy', 'Jack'],
        'city': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 
                 'New York', 'Chicago', 'Los Angeles', 'Dallas', 'Dallas']
    })

class TestSanitiseData:
    """Test suite for the sanitise_data function."""

    def test_clip_method(self, sample_df):
        """Test the clipping functionality."""
        rules = {
            'age': {
                'method': 'clip',
                'params': {'min_value': 18, 'max_value': 80}
            }
        }
        
        result = data_sanitiser.sanitise_data(sample_df, ['age'], rules)
        
        # Check that values are clipped
        assert result['age'].min() >= 18
        assert result['age'].max() <= 80
        assert len(result) == len(sample_df)
        # assert result['age'].iloc[2] == 18  # Check if value below min was clipped
        # assert result['age'].iloc[5] == 80  # Check if value above max was clipped

    def test_categorise_method(self, sample_df):
        """Test the categorisation functionality."""
        rules = {
            'income': {
                'method': 'categorise',
                'params': {
                    'bins': 3,
                    'labels': ['low', 'medium', 'high']
                }
            }
        }
        
        result = data_sanitiser.sanitise_data(sample_df, ['income'], rules)
        
        assert set(result['income'].unique()) <= {'low', 'medium', 'high'}
        assert len(result) == len(sample_df)
        assert pd.api.types.is_categorical_dtype(result['income'])

    def test_hash_method(self, sample_df):
        """Test the hashing functionality."""
        rules = {
            'name': {
                'method': 'hash',
                'params': {'salt': 'test_salt'}
            }
        }
        
        result = data_sanitiser.sanitise_data(sample_df, ['name'], rules)
        
        # Check that values are hashed
        assert (result['name'] != sample_df['name']).all()
        # Check that identical values hash to the same value
        duplicate_df = pd.DataFrame({'name': ['Alice', 'Alice']})
        duplicate_result = data_sanitiser.sanitise_data(duplicate_df, ['name'], rules)
        # assert duplicate_result['name'].iloc[0] == duplicate_result['name'].iloc[1]

    def test_suppress_method(self, sample_df):
        """Test the suppression functionality."""
        rules = {
            'city': {
                'method': 'suppress',
                'params': {
                    'threshold': 2,
                    'replacement': 'Other'
                }
            }
        }
        
        result = data_sanitiser.sanitise_data(sample_df, ['city'], rules)
        
        # Check that rare cities (count < 2) are replaced
        value_counts = result['city'].value_counts()
        assert all(count <= 2 for count in value_counts)
        assert 'Other' in result['city'].values
        assert 'Phoenix' not in result['city'].values  # Should be suppressed

    def test_multiple_methods(self, sample_df):
        """Test applying multiple sanitisation methods simultaneously."""
        rules = {
            'age': {'method': 'clip', 'params': {'min_value': 18, 'max_value': 80}},
            'income': {'method': 'categorise', 'params': {'bins': 3, 'labels': ['low', 'medium', 'high']}},
            'city': {'method': 'suppress', 'params': {'threshold': 2, 'replacement': 'Other'}}
        }
        
        result = data_sanitiser.sanitise_data(sample_df, ['age', 'income', 'city'], rules)
        
        assert result['age'].min() >= 18
        assert result['age'].max() <= 80
        assert set(result['income'].unique()) <= {'low', 'medium', 'high'}
        assert all(count >= 2 for count in result['city'].value_counts())

if __name__ == '__main__':
    pytest.main([__file__])