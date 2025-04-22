""" 
IO functions for IDX files. 

See also :py:mod:`bulum.op.idx_io_native`.
"""
import os
import shutil
import subprocess
import uuid

from bulum import utils

from .csv_io import *


def write_idx(df: pd.DataFrame, filename, cleanup_tempfile=True):
    """Write IDX file from dataframe, requires csvidx.exe."""
    if shutil.which('csvidx') is None:
        raise Exception("This method relies on the external program 'csvidx.exe'. Please ensure it is in your path.")
    temp_filename = f"{uuid.uuid4().hex}.tempfile.csv"
    write_area_ts_csv(df, temp_filename)
    command = f"csvidx {temp_filename} {filename}"
    process = subprocess.Popen(command)
    process.wait()
    if cleanup_tempfile:
        os.remove(temp_filename)


def write_area_ts_csv(df, filename, units="(mm.d^-1)"):
    """_summary_

    Parameters
    ----------
    df : DataFrame
    filename
    units : str, optional
        Defaults to "(mm.d^-1)".

    Raises
    ------
    Exception
        If shortened field names are going to clash in output file.
    """
    # ensures dataframe adheres to standards
    utils.assert_df_format_standards(df)
    # convert field names to 12 chars and check for collisions
    fields = {}
    for c in df.columns:
        c12 = f"{c[:12]:<12}"
        if c12 in fields.keys():
            raise Exception(f"Field names clash when shortened to 12 chars: {c} and {fields[c12]}")
        fields[c12] = c
    # create the header text
    header = f"{units}"
    for k in fields.keys():
        header += f',"{k}"'
    header += os.linesep
    header += "Catchment area (km^2)"
    for k in fields.keys():
        header += f", 1.00000000"
    header += os.linesep
    # open a file and write the header and the csv body
    with open(filename, "w+", newline='', encoding='utf-8') as file:        
        file.write(header)
        df.to_csv(file, header=False, na_rep=' NaN')
