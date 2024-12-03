import pandas as pd
import numpy as np
from typing import List, Union, Callable, Optional, Dict, Any

class IncrementalGroupbyAggregator:
    """
    Handles incremental aggregation of large datasets processed in chunks.
    
    Carefully merges chunk-level statistics to ensure correct final aggregation.
    """
    def __init__(self, group_columns: Union[str, List[str]], 
                 agg_column: str, 
                 agg_func: Union[str, Callable] = 'mean'):

        """
        Initialises an IncrementalGroupbyAggregator object.
        
        Parameters
        ----------
        group_columns : str or List[str]
            The columns to group by. If a single string, is interpreted as a
            single column to group by; if a List[str], is interpreted as a
            list of columns to group by.
        agg_column : str
            The column to aggregate.
        agg_func : str or Callable, optional
            The aggregation function to use. If a string, must be one of
            {'mean', 'sum', 'min', 'max', 'count'}; if a Callable, must take
            a pd.Series as input and return a pd.Series or pd.DataFrame.
            Defaults to 'mean'.
        """
        self.group_columns = [group_columns] if isinstance(group_columns, str) else group_columns
        self.agg_column = agg_column
        self.agg_func = agg_func
        
        # Internal storage for incremental computation
        self._group_stats: Dict[tuple, Dict[str, Any]] = {}
    
    def _merge_chunk_stats(self, existing: Dict[str, Any], 
                            new_chunk: Dict[str, Any]) -> Dict[str, Any]:

        """
        Merge chunk-level statistics into existing statistics.
        
        Parameters
        ----------
        existing : Dict[str, Any]
            The existing statistics to merge into.
        new_chunk : Dict[str, Any]
            The new chunk statistics to merge.
        
        Returns
        -------
        Dict[str, Any]
            The merged statistics.

        Raises
        ------
        ValueError
            If the aggregation function is not one of {'mean', 'sum', 'min', 'max', 'count'}.
        """
        if self.agg_func == 'mean':
            # Weighted average computation
            total_count = existing.get('count', 0) + new_chunk.get('count', 0)
            if total_count == 0:
                return new_chunk
            
            # Weighted average: (sum1/count1 * count1 + sum2/count2 * count2) / (count1 + count2)
            merged = {
                'sum': existing.get('sum', 0) + new_chunk.get('sum', 0),
                'count': total_count
            }
            return merged
        
        elif self.agg_func == 'sum':
            # Simple sum of chunk sums
            return {
                'sum': existing.get('sum', 0) + new_chunk.get('sum', 0)
            }
        
        elif self.agg_func == 'count':
            # Sum of counts across chunks
            return {
                'count': existing.get('count', 0) + new_chunk.get('count', 0)
            }
        
        elif self.agg_func == 'min':
            # Take the minimum across all chunks
            return {
                'min': min(existing.get('min', float('inf')), 
                           new_chunk.get('min', float('inf')))
            }
        
        elif self.agg_func == 'max':
            # Take the maximum across all chunks
            return {
                'max': max(existing.get('max', float('-inf')), 
                           new_chunk.get('max', float('-inf')))
            }
        
        else:
            raise ValueError(f"Unsupported aggregation function: {self.agg_func}")
    
    def process_chunk(self, chunk: pd.DataFrame):

        """
        Process a chunk of data by performing aggregation and updating internal statistics.

        This method processes a given data chunk by validating its columns, performing
        groupby aggregation based on the specified aggregation function, and merging the
        computed statistics into the internal storage for incremental aggregation.

        Parameters
        ----------
        chunk : pd.DataFrame
            A DataFrame representing a chunk of data to be processed. It must contain
            the columns specified in `self.group_columns` and `self.agg_column`.

        Raises
        ------
        ValueError
            If any of the required columns specified in `self.group_columns` or
            `self.agg_column` are not found in the chunk, or if the aggregation
            function is unsupported.
        """
        # Validate chunk
        for col in self.group_columns + [self.agg_column]:
            if col not in chunk.columns:
                raise ValueError(f"Column {col} not found in chunk")
        
        # Perform groupby aggregation on chunk
        if self.agg_func == 'mean':
            # Explicitly compute sum and count
            grouped = chunk.groupby(self.group_columns)
            chunk_stats = pd.DataFrame({
                'sum': grouped[self.agg_column].sum(),
                'count': grouped[self.agg_column].count()
            })
        elif self.agg_func == 'sum':
            chunk_stats = pd.DataFrame({
                'sum': chunk.groupby(self.group_columns)[self.agg_column].sum()
            })
        elif self.agg_func == 'min':
            chunk_stats = pd.DataFrame({
                'min': chunk.groupby(self.group_columns)[self.agg_column].min()
            })
        elif self.agg_func == 'max':
            chunk_stats = pd.DataFrame({
                'max': chunk.groupby(self.group_columns)[self.agg_column].max()
            })
        elif self.agg_func == 'count':
            chunk_stats = pd.DataFrame({
                'count': chunk.groupby(self.group_columns)[self.agg_column].count()
            })
        else:
            raise ValueError(f"Unsupported aggregation function: {self.agg_func}")
        
        # Merge chunk statistics
        for group, stats in chunk_stats.iterrows():
            # Convert stats to dictionary, handling different aggregation types
            if self.agg_func == 'mean':
                stats_dict = {'sum': stats['sum'], 'count': stats['count']}
            elif self.agg_func == 'sum':
                stats_dict = {'sum': stats['sum']}
            elif self.agg_func == 'count':
                stats_dict = {'count': stats['count']}
            elif self.agg_func == 'min':
                stats_dict = {'min': stats['min']}
            elif self.agg_func == 'max':
                stats_dict = {'max': stats['max']}
            
            if group in self._group_stats:
                self._group_stats[group] = self._merge_chunk_stats(
                    self._group_stats[group], stats_dict
                )
            else:
                self._group_stats[group] = stats_dict
    
    def get_final_result(self) -> pd.DataFrame:
        """
        Return the final result as a DataFrame after all chunks have been processed.

        After all chunks have been processed using `process_chunk`, this method
        returns a DataFrame containing the final result of the aggregation.
        The columns of the DataFrame include the group columns and the aggregated
        column with a name based on the specified aggregation function (e.g.
        'mean', 'sum', 'min', 'max', or 'count').

        Returns
        -------
        pd.DataFrame
            The final result of the aggregation.
        """
        results = []
        for group, stats in self._group_stats.items():
            result_row = dict(zip(self.group_columns, group))
            
            if self.agg_func == 'mean':
                # Compute weighted mean
                result_row['mean'] = stats.get('sum', 0) / stats.get('count', 1)
            elif self.agg_func == 'sum':
                result_row['sum'] = stats.get('sum', 0)
            elif self.agg_func == 'count':
                result_row['count'] = stats.get('count', 0)
            elif self.agg_func == 'min':
                result_row['min'] = stats.get('min', None)
            elif self.agg_func == 'max':
                result_row['max'] = stats.get('max', None)
            
            results.append(result_row)
        
        return pd.DataFrame(results)

# Example usage demonstrating correct chunk processing
def example_usage():
    # Simulate large dataset processing in chunks
    data_chunks = [
        pd.DataFrame({
            'H3': ['abc', 'abc', 'def'],
            'date': ['2023-01-01', '2023-01-01', '2023-01-02'],
            'speed': [50, 60, 55]
        }),
        pd.DataFrame({
            'H3': ['def', 'ghi', 'ghi'],
            'date': ['2023-01-02', '2023-01-03', '2023-01-03'],
            'speed': [65, 45, 40]
        })
    ]
