import itertools
import typing
from pathlib import Path

import numpy as np
import xarray as xr
from lgopy.core import DataReaderFactory

if typing.TYPE_CHECKING:
    from .scan import Scan


from pathlib import Path

def filter_scan_files(input_path: Path):
    """
    Filter the valid files in the input path based on supported extensions, case-insensitively.
    :param input_path: Path to the directory containing files to filter.
    :return: List of valid files with supported extensions.
    """
    # Ensure input path is a directory
    assert input_path.is_dir(), "Invalid path: the path must be a directory."

    # Initialize an empty list to store valid files
    list_files = []

    # Retrieve supported extensions and normalize them to lowercase
    supported_exts = {ext.lower() for ext in DataReaderFactory.registry.keys()}

    # Perform a case-insensitive search for each extension
    for file in input_path.rglob("*"):
        if file.suffix.lower() in supported_exts:
            list_files.append(file)

    return list_files



def merge_scan_files(scans_list_in: [typing.Tuple[Path, "Scan"]]) -> []:
    """
    Group the files by their extension.
    :param scans_list_in:
    :return:
    """
    scans_list_in = list(scans_list_in)
    # here we split the scans list into two lists, one for IDS scans and the other for the rest
    rest_scans, ids_scans = [], []

    while scans_list_in:
        file_path, scan = scans_list_in.pop(0)
        (rest_scans, ids_scans)[file_path.name.startswith("LID")].append(
            (file_path, scan)
        )

    # here we need to group the scans by folder and size
    def ids_scans_grouping_key(scan: typing.Tuple[Path, "Scan"]):
        """
        Group the scans by folder and size
        :param scan:
        :return:
        """
        scan_path, scan_obj = scan
        parent_folder = scan_path.parent.name
        scan_size = scan_obj.size
        scan_name_prefix = scan_path.stem[-4:]
        return parent_folder, scan_size, scan_name_prefix

    def rest_scans_grouping_key(scan: typing.Tuple[Path, "Scan"]):
        """
        Group the scans by folder and size
        :param scan:
        :return:
        """
        scan_path, scan_obj = scan
        parent_folder = scan_path.parent.name
        scan_size = scan_obj.size
        return parent_folder, scan_size

    # IDS scans
    scans_list_out = []
    for i, (group_key, group_files) in enumerate(
        group_scans_by(
            ids_scans,
            grouping_key=ids_scans_grouping_key,
        )
    ):
        parent_folder, scan_size, scan_name_prefix = group_key
        scan = concatenate_scans(group_files, name=parent_folder)
        scans_list_out.append((parent_folder, scan))

    # other providers scans
    for i, (group_key, group_files) in enumerate(
        group_scans_by(rest_scans, grouping_key=rest_scans_grouping_key)
    ):
        parent_folder, scan_size = group_key
        scan = concatenate_scans(group_files, name=parent_folder)
        scans_list_out.append((parent_folder, scan))

    return scans_list_out


def group_scans_by(scans_list: [typing.Tuple[Path, "Scan"]], grouping_key) -> []:
    """
    Group the list of files by the grouping key.
    :param scans_list: The list of files to group.
    :param grouping_key: is a function that returns a tuple of values
    :return:
    """
    # we use itertools.groupby to group the files by the grouping key

    sorted_list = sorted(scans_list, key=grouping_key)
    grouped_list = {
        key: list(group)
        for key, group in itertools.groupby(sorted_list, key=grouping_key)
    }
    for group_key, group_files in grouped_list.items():
        # for each group we sort the files withing the group based on name of the file
        group_files = list(sorted(group_files, key=lambda scan: scan[0].name))
        yield group_key, group_files


def concatenate_scans(scans_list: [typing.Tuple[Path, "Scan"]], name=None) -> []:
    """
    Concatenate the scans in the list.
    :param scans_list: The list of scans to concatenate.
    :return:
    """
    from .scan import Scan

    scans = list(map(lambda scan: scan[1]._xarr, scans_list))
    xarr = xr.concat(
        scans,
        dim="channels",
        combine_attrs="drop",
    )
    xarr.attrs = scans[0].attrs
    xarr.coords["channels"] = np.arange(0, xarr.shape[-1])
    xarr.name = name
    return Scan(xarr)
