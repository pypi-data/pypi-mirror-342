"""
IO functions for IQQM listquan. 
"""
import os

import numpy as np
import pandas as pd

from bulum import utils


def read_iqqm_lqn_output(filename, col_name=None, df=None, 
                         *, data_start_row=7) -> utils.TimeseriesDataframe:
    """
    Reads the output of IQQM listquan. This is a space-separated is format with
    two columns (date, value) and data starting on line 7.

    Parameters
    ----------
    filename 
        Path to the file to be read.
    col_name : optional
        If supplied, sets the name for the resulting output column, otherwise
        uses the filename.
    df : DataFrame, optional
        If supplied, joins the output to `df`.
    data_start_row : int, optional
        Optionally specify the start row; may be useful for reading other IQQM
        TEXT outputs.

    Returns
    -------
    utils.TimeseriesDataframe
    """
    # If no df was supplied, instantiate a new one
    if df is None:
        df = pd.DataFrame()
    # If no column name was specified, we use the base name of the file
    if col_name is None:
        col_name = os.path.basename(filename)
    # Read the data
    temp = pd.read_csv(filename, skiprows=(data_start_row-2),
                       sep=r'\s+', names=["Date", col_name], header=None)
    # temp = utils.set_index_dt(temp, format='%d/%m/%Y')
    temp.set_index(temp.columns[0], inplace=True)
    temp.index = utils.standardize_datestring_format(temp.index)
    temp.index.name = "Date"
    temp = temp.replace(r'^\s*$', np.nan, regex=True)
    df = df.join(temp, how="outer").sort_index()
    # TODO: THERE IS NO GUARANTEE THAT THE DATES OVERLAP, THEREFORE WE MAY END UP WITH A DATAFRAME WITH INCOMPLETE DATES
    # TODO: I SHOULD MAKE DEFAULT BEHAVIOUR AUTO-DETECT FORMAT DEPENDING ON *TYPE* AND *LOCATION* OF DELIMIT CHARS
    # TODO: In the meantime we use the below to assert that the format of the resulting df meets our minimum standards.
    utils.assert_df_format_standards(df)
    return utils.TimeseriesDataframe.from_dataframe(df)
