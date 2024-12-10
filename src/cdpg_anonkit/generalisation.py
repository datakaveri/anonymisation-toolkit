from typing import Tuple, Literal, Union, List, Optional, get_args
import pandas as pd
import numpy as np
import h3


class GeneraliseData:
    class SpatialGeneraliser:
        # TODO: rewrite so function can accept both dataframe with specified location column as well as series
        # helper function to clean coordinates attribute formatting

        @staticmethod
        def format_coordinates(series: pd.Series) -> Tuple[pd.Series, pd.Series]:
            """
            Clean coordinates attribute formatting.

            Takes a pandas Series of coordinates and returns a tuple of two Series: the first with the latitude, and the second with the longitude.

            The coordinates are expected to be in the format "[lat, lon]". The function will strip any leading or trailing whitespace and brackets from the coordinates,
            split them into two parts, and convert each part to a float.

            If the coordinate string is not in the expected format, a ValueError is raised.

            Parameters
            ----------
            series : pd.Series
                The series of coordinates to be cleaned.

            Returns
            -------
            Tuple[pd.Series, pd.Series]
                A tuple of two Series, one with the latitude and one with the longitude.
            """
            def parse_coordinate(coordinate: str) -> Tuple[float, float]:
                
                try:
                    lat, lon = coordinate.strip('[]').strip(' ').split(',')
                    return float(lat), float(lon)
                except (ValueError, IndexError) as e:
                    raise ValueError(f"Invalid coordinate format: {coordinate}") from e
            
            coordinates = series.apply(parse_coordinate)
            latitude = coordinates.apply(lambda x: x[0])
            longitude = coordinates.apply(lambda x: x[1])
            return latitude, longitude

        @staticmethod
        def generalise_spatial(latitude: pd.Series, longitude: pd.Series, spatial_resolution: int) -> pd.Series:
                       
            """
            Generalise a set of coordinates to an H3 index at a given resolution.

            Parameters
            ----------
            latitude : pd.Series
                The series of latitude values to be generalised.
            longitude : pd.Series
                The series of longitude values to be generalised.
            spatial_resolution : int
                The spatial resolution of the H3 index. Must be between 0 and 15.

            Returns
            -------
            pd.Series
                A series of H3 indices at the specified resolution.

            Raises
            ------
            ValueError
                If the spatial resolution is not between 0 and 15, or if the latitude or longitude values are not between -90 and 90 or -180 and 180 respectively.
            Warning
                If the length of the latitude and longitude series are not equal.
            """
            if not (0 <= spatial_resolution <= 15):
                raise ValueError("H3 Spatial resolution must be between 0 and 15.")
            
            if not latitude.between(-90, 90).all():
                raise ValueError("Latitude values must be between -90 and 90.")
            
            if not longitude.between(-180, 180).all():
                raise ValueError("Longitude values must be between -180 and 180.")
            
            if len(latitude) != len(longitude):
                raise Warning("Latitude and longitude series are of unequal length! Extra values will be ignored.")

            h3_index = [
                h3.latlng_to_cell(lat, lon, spatial_resolution)
                for lat, lon in zip(latitude, longitude)
            ]
            
            return pd.Series(h3_index, name='h3_index')

    class TemporalGeneraliser:

        @staticmethod     
        # TODO: Do we really need a wrapper around a standard pandas function?  
        # helper function to convert timestamp to pd.datetime object
        def format_timestamp(series: pd.Series) -> pd.Series:
            # Check if all timestamps in the series are of the same format
            """
            Convert a pandas Series of timestamps into datetime objects.

            This function takes a Series containing timestamp data and converts it into pandas datetime 
            objects. It handles mixed format timestamps and coerces any non-parseable values into NaT 
            (Not a Time).

            Parameters
            ----------
            series : pd.Series
                The input Series containing timestamp data to be converted.

            Returns
            -------
            pd.Series
                A Series where all timestamp values have been converted to datetime objects, with 
                non-parseable values set to NaT.
            """
            return pd.to_datetime(series, format='mixed', errors='coerce') # coerce non-parseable values to NaT
        
        # def __init__(self):
        #     self.temporal_resolution_args = Literal[15, 30, 60]
        @staticmethod       
        def generalise_temporal(data: Union[pd.Series, pd.DataFrame],
                                timestamp_col: str = None,
                                temporal_resolution: int = 60
                            ) -> pd.Series:
            """
            Generalise timestamp data into specified temporal resolutions.

            This function processes timestamp data, either in the form of a Series or a DataFrame,
            and generalises it into timeslots based on the specified temporal resolution. The resolution
            must be one of the following values: 15, 30, or 60 minutes.

            Parameters
            ----------
            data : Union[pd.Series, pd.DataFrame]
                The input timestamp data. Can be a pandas Series of datetime objects or a DataFrame
                containing a column with datetime data.
            timestamp_col : str, optional
                The name of the column containing timestamp data in the DataFrame. Must be specified
                if the input data is a DataFrame. Defaults to None.
            temporal_resolution : int, optional
                The temporal resolution in minutes for which the timestamps should be generalised.
                Allowed values are 15, 30, or 60. Defaults to 60.

            Returns
            -------
            pd.Series
                A pandas Series representing the generalised timeslots, with each entry formatted as
                'hour_minute', indicating the start of the timeslot.

            Raises
            ------
            AssertionError
                If the temporal resolution is not one of the allowed values (15, 30, 60).
            ValueError
                If `timestamp_col` is not specified when input data is a DataFrame, or if the specified
                column is not found in the DataFrame.
                If the timestamps cannot be converted to datetime objects.
            TypeError
                If the input data is neither a pandas Series nor a DataFrame.

            Example
            -------
            ### Using with a Series
            generalise_temporal(ts_series)
            
            ### Using with a DataFrame
            generalise_temporal(df, timestamp_col='timestamp')
            """
            temporal_resolution_args = Literal[15, 30, 60]
            
            # Validate temporal resolution
            options = list(get_args(temporal_resolution_args))
            assert temporal_resolution in options, (
                f"'{temporal_resolution}' is not in {options}, please choose a valid value"
            )
            
            # Extract the timestamp series based on input type
            if isinstance(data, pd.DataFrame):
                if timestamp_col is None:
                    raise ValueError(
                        "timestamp_col must be specified when input is a DataFrame"
                    )
                if timestamp_col not in data.columns:
                    raise ValueError(
                        f"Column '{timestamp_col}' not found in DataFrame. "
                        f"Available columns are: {list(data.columns)}"
                    )
                timestamp = data[timestamp_col]
            elif isinstance(data, pd.Series):
                timestamp = data
            else:
                raise TypeError(
                    f"Input must be pandas Series or DataFrame, not {type(data)}"
                )
            
            # Ensure timestamp data is datetime type
            try:
                timestamp = pd.to_datetime(timestamp)
            except Exception as e:
                raise ValueError(
                    f"Failed to convert input to datetime: {str(e)}"
                )
            
            # Extract date and time components
            time = timestamp.dt.time
            
            # Create timeslots
            timeslot = time.apply(
                lambda x: f'{x.hour}_{((x.minute)//temporal_resolution)*temporal_resolution}'
            )
            
            return pd.Series(timeslot, name='timeslot')

    class CategoricalGeneraliser:

        @staticmethod
        def generalise_categorical(data: pd.Series, bins: Union[int, List[float]], labels: Optional[List[str]] = None) -> pd.Series:
            """
            Generalise a categorical column by binning the values into categories.

            Parameters
            ----------
            data : pd.Series
                The input Series to be generalised.
            bins : Union[int, List[float]]
                The number of bins to use, or a list of bin edges.
            labels : Optional[List[str]], optional
                The labels to use for each bin. If not specified, the bin edges
                will be used as labels.

            Returns
            -------
            pd.Series
                The generalised Series.
            """
            return pd.cut(data, bins=bins, labels=labels)