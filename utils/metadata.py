# Made by: Yuri Yu
def metadata(df):
    import pandas as pd
    import numpy as np
    """
    Generate metadata for a pandas DataFrame.

    Parameters:
    df (DataFrame): The DataFrame for which to generate metadata.

    Returns:
    DataFrame: A DataFrame containing metadata such as column names, data types,
               missing values, unique values, basic statistics, etc.

    The function checks if the DataFrame is empty, computes the number of missing values and their percentage,
    calculates the number of unique values and their percentage, and provides basic statistics for numerical columns.
    It also lists the actual unique values for columns with fewer than 10 unique values.
    """
    if df.empty:
        return "DataFrame is empty"

    columns_list = list(df.columns.values)
    metadata = pd.DataFrame(columns_list, columns=['col_name'])

    # Data types
    metadata['data_type'] = df.dtypes.astype(str)

    # Missing values
    missing_values = df.isnull().sum()
    metadata['missing_values'] = missing_values

    # Missing values percentage
    metadata['missing_values_percentage'] = round(missing_values * 100 / df.shape[0], 2)
    
    # Number of unique values (numerical representation)
    unique_values_num = df.nunique()
    metadata['unique_values_num'] = unique_values_num

    # Number of unique values percentage
    metadata['unique_values_percentage'] = round(unique_values_num * 100 / df.shape[0], 2)

    # Unique values for columns with less than 10 unique values
    metadata['unique_values'] = [df[col].unique() if unique_values_num[col] < 10 else 'NA' for col in columns_list]

    # Basic statistics for interval columns (numerical types only)
    interval_columns = [col for col in columns_list if df[col].dtype in ['int64', 'float64']]
    if interval_columns:
        desc_interval = df[interval_columns].agg(['min', 'max', 'std']).transpose().reset_index().rename(columns={'index': 'col_name'})
        metadata = metadata.merge(desc_interval, on='col_name', how='left')

    return metadata

# Usage Example:
# metadata(df)