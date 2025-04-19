from typing import Optional, Union, List, Any, Set, Tuple, Dict
import pandas as pd

class Filter:
    """A class for filtering data in pandas DataFrames, lists, or sets.

    This class provides flexible filtering capabilities with support for:
    - Single value matching
    - Set-based filtering
    - Range-based filtering with min and max values
    - Combination of multiple filters
    """

    @classmethod
    def from_any(cls, column, values: Union[int, str, float, List, Tuple[Any, Any], Set, range]) -> 'Filter':
        """Creates a Filter instance from various input types.

        Args:
            column: The column name or value to filter on.
            values: The values to filter by. Can be:
                - A single value (int, str, float)
                - A list or set of values
                - A tuple of (min_value, max_value) for range filtering

        Returns:
            Filter: A configured Filter instance.

        Raises:
            ValueError: If a tuple is provided but doesn't have exactly 2 elements.
        """
        if isinstance(values, (list, set, range)):
            return cls(column=column, values=set(values))
        elif isinstance(values, tuple):
            if len(values) == 2:
                return cls(column=column, min_value=values[0], max_value=values[1])
            else:
                raise ValueError("Tuple must be of length 2")
        else:
            return cls(column=column, values=values)

    def __init__(self, column: str, values: Optional[Union[List[Any], Any]] = None, min_value: Optional[Any] = None, max_value: Optional[Any] = None):
        """Initialize a Filter instance.

        Args:
            column (str): The column name to filter on.
            values (Optional[Union[List[Any], Any]], optional): Values to match. Defaults to None.
            min_value (Optional[Any], optional): Minimum value for range filtering. Defaults to None.
            max_value (Optional[Any], optional): Maximum value for range filtering. Defaults to None.
        """
        self.column = column
        if isinstance(values, list):
            values = set(values)
        self.values = values
        self.min_value = min_value
        self.max_value = max_value

    def single_value(self) -> bool:
        """Check if the filter is configured for single value matching.

        Returns:
            bool: True if the filter is configured for single value matching.
        """
        return self.min_value is None and self.max_value is None and not isinstance(self.values, set)

    @property
    def value(self) -> Any:
        """Get the single value for this filter.

        Returns:
            Any: The single value if the filter is configured for single value matching.

        Raises:
            RuntimeError: If the filter has multiple values.
        """
        if self.single_value():
            return self.values
        else:
            raise RuntimeError("Filter has multiple values")

    def apply(self, data: Union[pd.DataFrame, List, Set]) -> Union[pd.DataFrame, List, Set]:
        """Apply the filter to the input data.

        Args:
            data (Union[pd.DataFrame, List, Set]): The data to filter.

        Returns:
            Union[pd.DataFrame, List, Set]: The filtered data.

        Raises:
            TypeError: If data is not a DataFrame, list, or set.
        """
        if isinstance(data, (list, set)):
            if self.values is not None:
                if isinstance(self.values, set):
                    data = [x for x in data if x in self.values]
                else:
                    data = [x for x in data if x == self.values]
            
            if self.min_value is not None:
                data = [x for x in data if x >= self.min_value]

            if self.max_value is not None:
                data = [x for x in data if x <= self.max_value]

            return data

        if not isinstance(data, pd.DataFrame):
            raise TypeError("data must be a pd.DataFrame or a list or a set")

        if self.column not in data.columns:
            return data
        
        if isinstance(self.values, set):
            data = data[data[self.column].isin(self.values)]
        elif self.values is not None:
            data = data[data[self.column] == self.values]

        if self.min_value is not None:
            data = data[data[self.column] >= self.min_value]

        if self.max_value is not None:
            data = data[data[self.column] <= self.max_value]

        return data
    
    def __and__(self, other) -> 'Filters':
        """Combine this filter with another filter or Filters instance.

        Args:
            other (Union[Filter, Filters]): The filter to combine with.

        Returns:
            Filters: A new Filters instance containing both filters.

        Raises:
            TypeError: If other is not a Filter or Filters instance.
        """
        if isinstance(other, Filter):
            return Filters([self, other])
        elif isinstance(other, Filters):
            return Filters([self] + other.filters)
        else:
            raise TypeError("other must be a Filter or Filters")
    
    def __rand__(self, other) -> 'Filters':
        """Right-hand version of the & operator.

        Args:
            other: The left-hand operand.

        Returns:
            Filters: A new Filters instance containing both filters.
        """
        return self & other

class Filters(Filter):
    """A class for combining multiple Filter instances.

    This class allows for combining multiple Filter instances into a single
    filter that can be applied to data.
    """

    def __init__(self, filters: Union[List[Filter], Dict[str, Filter]]):
        """Initialize a Filters instance.

        Args:
            filters (Union[List[Filter], Dict[str, Filter]]): List of Filter instances
                or dictionary of Filter instances.
        """
        self.filters = filters

    def __and__(self, other) -> 'Filters':
        """Combine this Filters instance with another filter or Filters instance.

        Args:
            other (Union[Filter, Filters]): The filter to combine with.

        Returns:
            Filters: A new Filters instance containing all filters.

        Raises:
            TypeError: If other is not a Filter or Filters instance.
        """
        if isinstance(other, Filter):
            return Filters(self.filters + [other])
        elif isinstance(other, Filters):
            return Filters(self.filters + other.filters)
        else:
            raise TypeError("other must be a Filter or Filters")
        
    def __rand__(self, other) -> 'Filters':
        """Right-hand version of the & operator.

        Args:
            other: The left-hand operand.

        Returns:
            Filters: A new Filters instance containing all filters.
        """
        return self & other

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply all filters in sequence to the input DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame to filter.

        Returns:
            pd.DataFrame: The filtered DataFrame.
        """
        for filter in self.filters:
            df = filter.apply(df)
        return df
