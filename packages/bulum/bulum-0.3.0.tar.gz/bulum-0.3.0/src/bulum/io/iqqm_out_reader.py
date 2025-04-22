"""Read .OUT files with an associated .IQN file."""

import os
import subprocess
from math import floor
from typing import Any, Literal, Optional

import numpy as np
import pandas as pd

from bulum import utils


class IqqmOutReader:
    """
    Examples
    --------
    .. code-block:: python

        reader = IqqmOutReader("abcd01.OUT")
        reader.require(node=1)
        reader.require(node=23)
        df = reader.read()
    """

    def __init__(self, iqqm_out_filepath) -> None:
        """
        Parameters
        ----------
        iqqm_out_filepath
            Path to the describing IQN file.
        """
        self.iqqm_out_filepath = iqqm_out_filepath
        # TODO replace iqqm_out_filepath with iqn_filepath
        self.iqqm_out_folder = os.path.dirname(self.iqqm_out_filepath)
        self.iqn_filepath = iqqm_out_filepath
        self.iqqm_out_basename = os.path.basename(self.iqqm_out_filepath)[:-4]
        self.required: dict[str, dict[str, Any]] = {}
        """A dictionary of all nodes marked as 'required' i.e. to be read."""
        self.available: dict[str, dict[str, Any]] = {}
        """A dictionary of all nodes that are available to be read based off the
        .OUT file."""

        # used for Python reader
        self._out_node_order: dict[int, list[str]] = {}
        """Maps node supertypes to the order in which data occurs in the
        corresponding .OUT file, identified by node number and output number
        (i.e. column of the recording matrix).
        """

        # used for IQQMGUI call
        self._lqn_filename: Optional[str] = None
        self._lqn_filepath: Optional[str] = None
        self._csv_filename: Optional[str] = None
        self._csv_filepath: Optional[str] = None
        self._start_dt_str: Optional[str] = None
        self._end_dt_str: Optional[str] = None
        self._files_requiring_cleanup: list[str] = []

        self._search_available_data()

    # pylint: disable=w0622
    def require(self, node: Optional[int | str] = None,
                supertype: Optional[float] = None, type: Optional[float] = None,
                output: Any = None) -> bool:
        """Mark a node or multiple nodes as 'required' i.e. for reading.
        At least one argument must be non-null.

        Returns
        -------
        bool
            `True` if at least one node was marked, `False` otherwise, likely
            indicating failure or a bad node specification.
        """
        if node is None and supertype is None and type is None and output is None:
            raise ValueError("At least one argument to require() must be non-null")
        # Coerce node and output into string formats padded with zeros.
        node = None if node is None else f"{node:0>3}"
        output = None if output is None else f"{output:0>2}"
        pre_num_nodes = len(self.required)
        # Now loop over all available records and identify the ones required by the user.
        for k, v in self.available.items():
            if (
                ((node is None) or (node == v["node"])) and
                ((supertype is None) or (supertype == v["supertype"])) and
                ((type is None) or (type == v["type"])) and
                ((output is None) or (output == v["output"]))
            ):
                self.required[k] = v
        return pre_num_nodes > len(self.required)

    def read(self, remove_temp_files=True, read_all_availabe=False, *,
             engine: Literal["iqqmgui", "python"] = "iqqmgui", iqqmgui_path=None) -> pd.DataFrame:
        """
        Invoke the class to read the associated data.

        Parameters
        ----------
        remove_temp_files : bool
            Clean up after yourself (remove artifacts from running ``iqmgui``).
        read_all_available : bool
            Read all nodes instead of just those previously marked by the user
            as required.
        engine : "iqqmgui" or "python"
            Decides how to parse the OUT file data. `"iqqmgui"` will call on the
            executable (on path or provided by `iqqmgui_path`), while `python`
            will use the bulum native implementation.
        iqqmgui_path : str, optional
            If `engine` is set to `iqqmgui`, you can specify the executable to
            use to extract data.

        Returns
        -------
        pandas.DataFrame
        """
        if engine == "iqqmgui":
            if read_all_availabe:
                required_memo = self.required
                self.required = self.available
            self._write_iqqmgui_lqn_file()
            self._call_iqqmgui_lqn(iqqmgui_path=iqqmgui_path)
            answer = self._read_iqqmgui_csv()
            if remove_temp_files:
                self._clean_up()
            if read_all_availabe:
                # Remember previous settings
                self.required = required_memo
        elif engine == "python":
            answer = self._py_read_out(read_all=read_all_availabe)
        else:
            raise ValueError(f"Invalid argument: {engine=}")

        return answer

    def _search_available_data(self) -> None:
        """
        Searches the .IQN file for data.
        """
        with open(self.iqqm_out_filepath, mode="r", encoding="UTF-8") as file:
            ss = file.readlines()
        # Read the recorder-flag matrix
        ss2 = ss[2].split()  # line 3 in the file
        n_node_types = int(ss2[0])
        n_output_types = int(ss2[1])
        recorder_flags: list[list] = []
        for i in range(n_node_types):
            recorder_line = ss[3 + i].split()
            recorder_flags.append(recorder_line[0:n_output_types])
            self._out_node_order[i] = []

        # Read the date range
        ssx = ss[n_node_types + 3].split()  # 01/01/1890 31/12/2008  0
        self._start_dt_str = ssx[0].replace('/', ' ')
        self._end_dt_str = ssx[1].replace('/', ' ')

        # Read all the nodes (loop over the nodes)
        for i in range(n_node_types + 4, len(ss)):
            node_line = ss[i]
            if node_line.strip() == "":
                break
            node_number: str = f"{int(node_line[0:3]):0>3}"  # 053
            node_name = str.strip(node_line[3:20])  # 'Unallocated Irr'
            node_type = float(node_line[20:])  # 8.3
            node_supertype = floor(node_type)  # 8
            for j in range(n_output_types):
                if recorder_flags[node_supertype][j] == "0":
                    continue
                recorder_number = f"{j + 1:0>2}"  # 03; recorder numbers start at 1

                node_recorder_ident = f"{node_number}_{recorder_number}.d"
                self._out_node_order[node_supertype].append(node_recorder_ident)
                self.available[node_recorder_ident] = {
                    "node": node_number,
                    "supertype": node_supertype,
                    "type": node_type,
                    "output": recorder_number,
                    "node_name": node_name,
                }

    # -----------------------------
    # ----- CONVENIENCE FUNCS -----
    # -----------------------------

    def num_to_name(self, *, which: Literal["required", "available"] = "required"
                    ) -> dict[str, str]:
        """Return a mapping between node numbers and (IQQM) names. 

        Purely here for convenience in cross-referencing nodes."""
        src: dict[str, dict[str, str]] = {}
        match which:
            case "required":
                src = self.required

            case "available":
                src = self.available

            case _:
                raise ValueError("Invalid `which` argument to IqqmOutReader.num_to_name()")

        d: dict[str, str] = {}
        for node_info in src.values():
            d[node_info["node"]] = node_info["node_name"]
        return d

    # -----------------------------
    # --- NATIVE PYTHON READER ----
    # -----------------------------

    def _py_read_out(self, *, read_all=False) -> pd.DataFrame:
        """python engine: reads out all required data"""
        if read_all:
            search_dict = self.available
        else:
            search_dict = self.required

        required_supertypes = set()
        for node in search_dict.values():
            required_supertypes.add(node["supertype"])

        df: Optional[pd.DataFrame] = None
        for supertype in required_supertypes:
            suffix = f"{supertype:0>2}.OUT"
            path = self.iqn_filepath[:-4] + suffix
            temp_df = self._py_read_single_out_file(path, supertype)
            if df is None:
                df = temp_df
            else:
                df = df.join(temp_df)

        assert df is not None
        if not read_all:
            required_names = list(self.required.keys())
            df = df[required_names]

        # set index to dates
        assert self._start_dt_str and self._end_dt_str
        start_dt = pd.to_datetime(self._start_dt_str, dayfirst=True)
        end_dt = pd.to_datetime(self._end_dt_str, dayfirst=True)
        date_range = pd.date_range(start_dt, end_dt, inclusive="both")
        df["Date"] = date_range.map(lambda x: x.strftime(r"%Y-%m-%d"))
        df.set_index("Date", inplace=True)
        df = df.astype(np.float64)
        utils.assert_df_format_standards(df)
        return df

    def _py_read_single_out_file(self, path, supertype: int) -> pd.DataFrame:
        """python engine: read a single .OUT file.

        Parameters
        ----------
        path
            Path to the .OUT file
        supertype
            Supertype of node(s) of interest. Used to specify which ordered
            nodes to grab data for.
        """
        output_order = self._out_node_order[supertype]
        data_types = [(name, 'f4') for name in output_order]
        data = np.fromfile(path, offset=4, dtype=data_types)
        df = pd.DataFrame(data)
        return df

    # -----------------------------
    # ------ IQQMGUI READER -------
    # -----------------------------

    def _write_iqqmgui_lqn_file(self) -> None:
        """Generates an iqqmgui lqn file so that we can use iqqm to extract data to csv."""
        self._lqn_filename = "temp.run"
        self._lqn_filepath = f"{self.iqqm_out_folder}/{self._lqn_filename}"
        with open(self._lqn_filepath, "w+", encoding='utf-8') as file:
            # pylint: disable=c0301
            file.write("Listing file generated by bulum\n")
            file.write(f"{self._start_dt_str} {self._end_dt_str} /\n")  # 01 01 1890 31 12 2008 / start date, end date
            file.write(f"'{self.iqqm_out_basename}' /\n")  # 'O02l' / Name of IQN File
            file.write(f"{len(self.required)} 0 1 /\n")  # 17 0 1 /no files, no eqns, (no csv ?)
            i = 0
            for k, v in self.required.items():
                i += 1
                iqqm_ts_filepath = f"{self.iqqm_out_folder}/{k}"
                self._files_requiring_cleanup.append(iqqm_ts_filepath)
                file.write(f"'{k}' 00 00 00 00 T / {[i]}\n")  # 'O02l#030.01d' 00 00 00 00 T / [1]
                file.write("1 0 0 /\n")  # 1 0 0 /
                file.write(f"{v['node']} {v['output']} /\n")  # 030 1 /
            self._csv_filename = "temp.csv"
            self._csv_filepath = f"{self.iqqm_out_folder}/{self._csv_filename}"
            file.write(f"{self._csv_filename} /\n")  # DW_Diversions.csv /
            file.write(f"1-{i} /\n")  # 1-17 /
        self._files_requiring_cleanup.append(self._lqn_filepath)

    def _call_iqqmgui_lqn(self, *, iqqmgui_path=None) -> None:
        """Uses iqqmgui to extract data to csv.

        Parameters
        ----------
        iqqmgui_path
            Allows specification of a particular iqqmgui executable.
        """
        if self._csv_filepath is None:
            raise RuntimeError("Order of operations: method called before csv written.")

        if iqqmgui_path:
            process = subprocess.Popen(f"{iqqmgui_path} {self._lqn_filename}",
                                       cwd=f"{self.iqqm_out_folder}")
        else:
            process = subprocess.Popen(f"iqmgui {self._lqn_filename}",
                                       cwd=f"{self.iqqm_out_folder}")
        process.wait()
        self._files_requiring_cleanup.append(self._csv_filepath)
        self._files_requiring_cleanup.append(f"{self.iqqm_out_folder}/iqqmml.txt")
        # ^^^ Artifact from running iqmgui

    def _read_iqqmgui_csv(self) -> pd.DataFrame:
        """Reads the csv from iqqmgui into a dataframe."""
        if self._csv_filepath is None:
            raise RuntimeError("Order of operations: method called before csv written.")
        df = pd.read_csv(self._csv_filepath)
        df.columns = ["Date"] + [c.strip() for c in df.columns[1:]]  # type: ignore
        # df = utils.set_index_dt(df)
        df.set_index("Date", inplace=True)
        utils.assert_df_format_standards(df)
        return df

    def _clean_up(self) -> None:
        """Removes any file-artifacts created by this class."""
        for f in self._files_requiring_cleanup:
            os.remove(f)
        self._files_requiring_cleanup.clear()


class iqqm_out_reader(IqqmOutReader):  # pylint: disable=invalid-name
    """
    For backwards compatibility. See :class:`IqqmOutReader`.

    .. deprecated:: 0.3.0
        Non-pythonic naming 
    """
