import pytest
import pandas as pd
import numpy as np

import src.cdpg_anonkit.sanitisation as sanitisation

sanitiser = sanitisation.SanitiseData

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
        
        result = sanitiser.sanitise_data(sample_df, ['age'], rules)
        
        # Check that values are clipped
        assert result['age'].min() >= 18
        assert result['age'].max() <= 80
        assert len(result) == len(sample_df)
        # assert result['age'].iloc[2] == 18  # Check if value below min was clipped
        # assert result['age'].iloc[5] == 80  # Check if value above max was clipped


    def test_hash_method(self, sample_df):
        """Test the hashing functionality."""
        rules = {
            'name': {
                'method': 'hash',
                'params': {'salt': 'test_salt'}
            }
        }
        
        result = sanitiser.sanitise_data(sample_df, ['name'], rules)
        
        # Check that values are hashed
        assert (result['name'] != sample_df['name']).all()
        # # Check that identical values hash to the same value
        # duplicate_df = pd.DataFrame({'name': ['Alice', 'Alice']})
        # duplicate_result = data_sanitiser.sanitise_data(duplicate_df, ['name'], rules)
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
        
        result = sanitiser.sanitise_data(sample_df, ['city'], rules)
        
        # Check that rare cities (count < 2) are replaced
        value_counts = result['city'].value_counts()
        assert all(count <= 2 for count in value_counts)
        assert 'Other' in result['city'].values
        assert 'Phoenix' not in result['city'].values  # Should be suppressed

    def test_multiple_methods(self, sample_df):
        """Test applying multiple sanitisation methods simultaneously."""
        rules = {
            'age': {'method': 'clip', 'params': {'min_value': 18, 'max_value': 80}},
            'city': {'method': 'suppress', 'params': {'threshold': 2, 'replacement': 'Other'}}
        }
        
        result = sanitiser.sanitise_data(sample_df, ['age', 'city'], rules)
        
        assert result['age'].min() >= 18
        assert result['age'].max() <= 80
        assert all(count >= 2 for count in result['city'].value_counts())

    def test_error_handling(self, sample_df):
        """Test error handling for various invalid inputs."""
        
        # Test invalid column name
        with pytest.raises(ValueError, match="Column 'invalid_column' not found"):
            sanitiser.sanitise_data(sample_df, ['invalid_column'], {'invalid_column': {'method': 'clip'}})
        
        # Test invalid method
        with pytest.raises(ValueError, match="Unknown sanitisation method"):
            sanitiser.sanitise_data(sample_df, ['age'], {'age': {'method': 'invalid_method'}})
        
        # Test missing required parameters for clip
        with pytest.raises(KeyError):
            sanitiser.sanitise_data(sample_df, ['age'], {'age': {'method': 'clip', 'params': {}}})

    def test_empty_dataframe(self):
        """Test handling of empty DataFrame."""
        empty_df = pd.DataFrame(columns=['age', 'income', 'name', 'city'])
        rules = {
            'age': {'method': 'clip', 'params': {'min_value': 18, 'max_value': 80}}
        }
        
        result = sanitiser.sanitise_data(empty_df, ['age'], rules)
        assert len(result) == 0
        assert list(result.columns) == list(empty_df.columns)

if __name__ == '__main__':
    pytest.main([__file__])