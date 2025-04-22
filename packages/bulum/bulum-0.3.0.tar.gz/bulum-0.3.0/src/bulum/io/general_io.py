""" 
General use IO functions.
"""
import re

import bulum.io as bio
from bulum import utils


def read(filename: str, **kwargs) -> utils.TimeseriesDataframe:
    """
    Read the input file.

    It will attempt to determine the filetype and dispatch to the appropriate
    function in `bulum.io`.
    """
    filename_lower = filename.lower()
    df = None
    if filename_lower.endswith(".res.csv"):
        df = bio.read_res_csv(filename, **kwargs)
        if df is None:
            raise ValueError("Res csv could not be read.")
    elif filename_lower.endswith(".csv"):
        df = bio.read_ts_csv(filename, **kwargs)
    elif filename_lower.endswith(".idx"):
        df = bio.read_idx(filename, **kwargs)
    elif re.search(".[0-9]{2}d$", filename_lower):
        df = bio.read_iqqm_lqn_output(filename, **kwargs)
    else:
        raise ValueError(f"Unknown file extension: {filename}")
    assert isinstance(df, utils.TimeseriesDataframe), \
        "Output of `read` is not a TimeseriesDataframe."
    return df
