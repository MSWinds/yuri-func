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
    metadata['data_type'] = [i for i in df.dtypes.astype(str)]

    # Missing values
    metadata['missing_values'] = [i for i in df.isnull().sum()]

    # Missing values percentage
    metadata['missing_values_percentage'] =  [round(i*100,2) for i in df.isnull().sum() / df.shape[0]]
    
    # Number of unique values (numerical representation)
    unique_values_num = df.nunique()
    metadata['unique_values_num'] = [i for i in unique_values_num]

    # Number of unique values percentage [round(i*100,2) for i in df.nunique() / df.shape[0]]
    metadata['unique_values_percentage'] = [round(i*100,2) for i in df.nunique() / df.shape[0]]

    # Unique values for columns with less than 10 unique values
    metadata['unique_values'] = [df[col].unique() if unique_values_num[col] <= 10 else 'NA' for col in columns_list]

    # Basic statistics for interval columns (numerical types only)
    interval_columns = [col for col in columns_list if df[col].dtype in ['int64', 'float64', 'int32', 'float32', 'int16', 'float16', 'int8', 'float8', 'int', 'float', 'double']]
    if interval_columns:
        desc_interval = df[interval_columns].describe().transpose().reset_index().rename(columns={'index': 'col_name'})
        desc_interval = desc_interval[['col_name', 'min', 'max', 'std']]
        metadata = metadata.merge(desc_interval, on='col_name', how='left')

    return metadata

# Usage Example:
# metadata(df)