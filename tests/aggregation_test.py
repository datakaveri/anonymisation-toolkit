import pytest
import pandas as pd
import numpy as np
from typing import List, Union, Callable

from src.cdpg_anonkit.aggregation import IncrementalGroupbyAggregator
@pytest.fixture
def test_itms_type_data(): 
    data_chunks = [
        pd.DataFrame({
            'H3': ['abc', 'abc', 'def', 'ghi'],
            'date': ['2023-01-01', '2023-01-01', '2023-01-02', '2023-01-03'],
            'license_plate': ['ABC123', 'ABC123', 'ABC123', 'ABC123'],
            'speed': [50, 60, 60, 70]
        }),
        pd.DataFrame({
            'H3': ['jkl', 'mno', 'pqr'],
            'date': ['2023-01-02', '2023-01-03', '2023-01-04'],
            'license_plate': ['ABC123', 'ABC123', 'ABC123'],
            'speed': [55, 65, 75]
        }),
        pd.DataFrame({
            'H3': ['rst', 'uvw', 'xyz'],
            'date': ['2023-01-02', '2023-01-03', '2023-01-05'],
            'license_plate': ['ABC123', 'ABC123', 'ABC123'],
            'speed': [45, 85, 95]
        }),
        pd.DataFrame({
            'H3': ['abc', 'def', 'ghi'],
            'date': ['2023-01-01', '2023-01-02', '2023-01-03'],
            'license_plate': ['DEF456', 'DEF456', 'DEF456'],
            'speed': [40, 50, 60]
        }),
        pd.DataFrame({
            'H3': ['jkl', 'mno', 'pqr'],
            'date': ['2023-01-02', '2023-01-03', '2023-01-04'],
            'license_plate': ['DEF456', 'DEF456', 'DEF456'],
            'speed': [45, 55, 65]
        })
    ]
    return data_chunks
    
def test_multi_column_mean_aggregation(test_itms_type_data):
    """
    Test mean aggregation with a single group column
    """
    aggregator = IncrementalGroupbyAggregator(group_columns=['H3', 'date', 'license_plate'],
                                              agg_column = 'speed',
                                              agg_func='mean')
    
    data_chunks = test_itms_type_data
    for chunk in data_chunks:
        aggregator.process_chunk(chunk)

    
    # Get final result
    result = aggregator.get_final_result()
    
    # Convert result to a dictionary for easier verification
    result_dict = result.set_index(['H3', 'date', 'license_plate'])['mean'].to_dict()
    
    # Manually calculated expected values
    expected_values = {
        ('abc', '2023-01-01', 'ABC123'): 55,
        ('def', '2023-01-02', 'ABC123'): 60,
        ('ghi', '2023-01-03', 'ABC123'): 70,
        ('jkl', '2023-01-02', 'ABC123'): 55,
        ('mno', '2023-01-03', 'ABC123'): 65,
        ('pqr', '2023-01-04', 'ABC123'): 75,
        ('rst', '2023-01-02', 'ABC123'): 45,
        ('uvw', '2023-01-03', 'ABC123'): 85,
        ('xyz', '2023-01-05', 'ABC123'): 95,
        ('abc', '2023-01-01', 'DEF456'): 40,
        ('def', '2023-01-02', 'DEF456'): 50,
        ('ghi', '2023-01-03', 'DEF456'): 60,
        ('jkl', '2023-01-02', 'DEF456'): 45,
        ('mno', '2023-01-03', 'DEF456'): 55,
        ('pqr', '2023-01-04', 'DEF456'): 65
    }
    
    # Verify the results
    for key, expected_mean in expected_values.items():
        assert result_dict[key] == pytest.approx(expected_mean), f"Mismatch for key {key}"
    
    # Optionally, verify the total number of unique groups
    assert len(result) == len(expected_values)
def test_other_aggregation_functions():
    """
    Test sum, min, max, and count aggregation functions
    """
    agg_funcs = ['sum', 'min', 'max', 'count']
    
    for func in agg_funcs:
        aggregator = IncrementalGroupbyAggregator('category', 'value', agg_func=func)
        
        # Chunk 1
        chunk1 = pd.DataFrame({
            'category': ['A', 'A', 'B', 'B'],
            'value': [10, 20, 30, 40]
        })
        aggregator.process_chunk(chunk1)
        
        # Chunk 2
        chunk2 = pd.DataFrame({
            'category': ['A', 'B', 'C'],
            'value': [15, 25, 50]
        })
        aggregator.process_chunk(chunk2)
        
        # Get final result
        result = aggregator.get_final_result()
        
        # Verify results based on aggregation function
        result_dict = result.set_index('category')[func].to_dict()
        
        if func == 'sum':
            assert result_dict['A'] == 45
            assert result_dict['B'] == 95
            assert result_dict['C'] == 50
        elif func == 'min':
            assert result_dict['A'] == 10
            assert result_dict['B'] == 25
            assert result_dict['C'] == 50
        elif func == 'max':
            assert result_dict['A'] == 20
            assert result_dict['B'] == 40
            assert result_dict['C'] == 50
        elif func == 'count':
            assert result_dict['A'] == 3
            assert result_dict['B'] == 3
            assert result_dict['C'] == 1

def test_error_handling():
    """
    Test error handling for invalid inputs
    """
    with pytest.raises(ValueError, match="Unsupported aggregation function"):
        IncrementalGroupbyAggregator('category', 'value', agg_func='invalid_func')
    
    # Test missing columns
    aggregator = IncrementalGroupbyAggregator('category', 'value', 'min')
    
    with pytest.raises(ValueError, match="Column category not found in chunk"):
        aggregator.process_chunk(pd.DataFrame({'wrong_column': [1, 2, 3]}))

def test_empty_chunk_handling():
    """
    Test handling of empty chunks
    """
    aggregator = IncrementalGroupbyAggregator('category', 'value')
    
    # Empty chunk
    chunk = pd.DataFrame(columns=['category', 'value'])
    aggregator.process_chunk(chunk)
    
    result = aggregator.get_final_result()
    assert len(result) == 0

def test_custom_aggregation_function():
    """
    Test custom aggregation function (not implemented in the current class)
    """
    # Note: This test will fail with the current implementation
    # It demonstrates a potential extension of the class
    with pytest.raises(ValueError):
        custom_func = lambda x: x.median()
        aggregator = IncrementalGroupbyAggregator('category', 'value', agg_func=custom_func)