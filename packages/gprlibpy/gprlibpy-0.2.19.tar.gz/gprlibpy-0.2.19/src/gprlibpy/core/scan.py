import io
import typing
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed, ProcessPoolExecutor
from typing import Union
from pathlib import Path
from lgopy.core import DataReaderFactory
from skyio import GenericPath, CloudPath
import xarray  as xr
import logging
from .utils import merge_scan_files
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
from PIL.Image import Image as PILImageType

from ..utils import FileUtils, StretchingFunction, ImageOutputFormat
from ..utils.image_utils import to_image
from .dataset import Dataset

logger = logging.getLogger(__name__)

class Scan:
    """
    A class to represent a GPR scan.
    """
    def __init__(self, xarr: xr.DataArray):
        self._xarr: xr.DataArray = xarr

    @property
    def name(self):
        """
        Get the name of the scan
        :return: name of the scan
        """
        return self._xarr.name

    @property
    def values(self):
        """
        Get the data of the scan
        :return:
        """
        return self._xarr.values

    @property
    def coords(self):
        """
        Get the coordinates of the scan
        :return:
        """
        return self._xarr.coords

    @property
    def dims(self):
        """
        Get the dimensions of the scan
        :return:
        """
        return self._xarr.dims

    @property
    def attrs(self):
        """
        Get the attributes of the scan
        :return:
        """
        return self._xarr.attrs

    @property
    def size(self):
        """
        Get the size of the scan
        :return: size of the scan
        """
        return self._xarr.size

    @property
    def shape(self):
        """
        Get the shape of the scan
        :return: shape of the scan
        """
        return self._xarr.shape

    @property
    def num_channels(self):
        """
        Get the number of channels in the scan
        :return: number of channels
        """
        return self._xarr.shape[-1]

    @property
    def num_samples(self):
        """
        Get the number of samples in the scan
        :return: number of samples
        """
        return self._xarr.shape[0]

    @property
    def num_traces(self):
        """
        Get the number of traces in the scan
        :return: number of traces
        """
        return self._xarr.shape[1]

    @property
    def xarr(self):
        """
        Get the xarray object
        :return: xarray object
        """
        return self._xarr

    def __getitem__(self, key):
        """
        Get the item from the scan object using the xarray indexing syntax (https://xarray.pydata.org/en/stable/indexing.html)
        :param key:
        :return:
        """
        x_arr = self._xarr.__getitem__(key)
        return Scan(x_arr)

    def __setitem__(self, key, value):
        """
        Set the item in the scan object using the xarray indexing syntax (https://xarray.pydata.org/en/stable/indexing.html)
        :param key:
        :param value:
        :return:
        """
        self._xarr.__setitem__(key, value)

    def __repr__(self):
        """
        Return the string representation of the scan object based on the xarray representation
        """
        return self._xarr.__repr__()

    def to_numpy(self):
        """convert the scan object into a native numpy array"""
        data_arr = self._xarr.data.copy()
        return data_arr


    @classmethod
    def from_path(cls, file_path: Union[str, Path, GenericPath], **kwargs):
        """
        Create a Scan object from a file.

        :param file_path: File path as a string, Path object, or GenericPath. Can be local or a GCP bucket.
        :param kwargs: Additional keyword arguments passed to file loaders.
        :return: A Scan object or Dataset depending on the file type.
        :raises ValueError: If the file format is unsupported.
        """
        file_path = GenericPath(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"File or directory not found: {file_path}")

        # Extract file extension
        file_extension = file_path.suffix.lower()

        # Handle supported file types
        if file_extension == ".zarr":
            ds_xarr = xr.open_zarr(file_path)
            xarr = (ds_xarr.to_array()
                    .squeeze("variable")
                    .drop_vars("variable", errors="ignore"))
            return Scan(xarr) if len(ds_xarr.data_vars) == 1 else Dataset(ds_xarr)

        if file_extension == ".nc":
            return Scan(xr.open_dataarray(file_path))

        # Handle directory-based scans
        if file_path.is_dir():
            return cls.__from_folder(file_path, **kwargs)

        # Handle other file types
        if file_extension:
            return cls.__from_file(file_path, **kwargs)

        raise ValueError(f"Unsupported file type: {file_extension}. Supported formats: .zarr, .nc")


    @classmethod
    def __from_folder(cls, folder_path: Path, **kwargs):
        """
        Create a Scan or Dataset object from a folder.

        :param folder_path: Folder path (local or GCP bucket).
        :param kwargs: Additional parameters (e.g., merge_channels, return_dataset).
        :return: A list of Scan objects, a single Dataset, or an xarray.Dataset.
        """
        # Collect all file paths
        all_paths = list(Path(folder_path).rglob("*"))

        # Initialize storage for processed surveys
        gpr_surveys = []

        # Use ThreadPoolExecutor for parallel processing
        with ThreadPoolExecutor(max_workers=min(8, len(all_paths))) as executor:
            futures = {executor.submit(cls.from_path, file_path, **kwargs): file_path for file_path in all_paths}

            for future in as_completed(futures):
                task_exception = future.exception()
                file_path = futures[future]
                if task_exception:
                    logger.error(
                        f"error reading the file {file_path}: {task_exception}"
                    )
                    continue
                task_result = future.result()
                gpr_surveys.append((file_path, task_result))


        if not gpr_surveys:
            raise ValueError("No valid scan files found in the folder.")

        # Separate scans and datasets
        scan_list = [(fp, survey) for fp, survey in gpr_surveys if isinstance(survey, Scan)]
        dataset_list = [(fp, survey) for fp, survey in gpr_surveys if isinstance(survey, Dataset)]
        merge_channels = kwargs.pop("merge_channels", True)

        # Merge B-scans if needed
        if merge_channels:
            c_scans, b_scans = [], []
            while scan_list:
                file_path, scan = scan_list.pop(0)
                (c_scans, b_scans)[scan.num_channels == 1].append((file_path, scan))
            if b_scans:
                scan_list.extend(merge_scan_files(b_scans))

        # Handle cases where only one scan or dataset remains
        if len(dataset_list) == 1 and not scan_list:
            return dataset_list[0][1]
        if len(scan_list) == 1 and not dataset_list:
            return scan_list[0][1]

        # Return combined list of scans and datasets
        return [scan for _, scan in scan_list] + [dataset for _, dataset in dataset_list]

    @classmethod
    def __from_file(cls, file_path: GenericPath, **kwargs):
        """
        Create a Scan object from a file
        :param file_path: file path
        :return:
        """

        logger.debug(f"Creating a new Scan object from a file {file_path}.")
        assert file_path.exists(), f"File {file_path} does not exist."
        file_ext = file_path.suffix.lower()
        supported_exts = ",".join(DataReaderFactory.registry.keys()) + ".nc"
        assert file_ext in DataReaderFactory.registry, (
            "Invalid file extension. "
            f"Only files with extension in the following list are supported: {supported_exts}"
        )
        # read the file
        reader = DataReaderFactory.build(file_path.suffix, **kwargs)
        data_xarr = reader(file_path)
        scan = Scan(data_xarr)
        return scan


    @classmethod
    def from_uri(cls, uri: str):
        """
        Create a Scan object from a URL
        :param uri: URL
        :return: Scan object
        """
        cloud_file = CloudPath(uri)
        content_type = cloud_file.content_type

        if content_type == "application/zip":
            return cls._from_zip(cloud_file)
        elif content_type == "application/x-netcdf":
            return cls._from_netcdf(cloud_file)
        else:
            raise ValueError(f"Unsupported content type: {content_type}")

    @classmethod
    def _from_zip(cls, cloud_file: CloudPath):
        """
        Create a Scan object from a zip file
        :param cloud_file: CloudPath object
        :return: Scan object
        """
        file_bytes = cloud_file.read_bytes()
        file_buffer = io.BytesIO(file_bytes)
        with FileUtils.onflyTemporaryDirectory() as temp_dir:
            with zipfile.ZipFile(file_buffer) as zip_ref:
                zip_ref.extractall(temp_dir)
            return cls.from_path(temp_dir)

    @classmethod
    def _from_netcdf(cls, cloud_file: CloudPath):
        """
        Create a Scan object from a NetCDF file
        :param cloud_file: CloudPath object
        :return: Scan object
        """
        file_bytes = cloud_file.read_bytes()
        file_buffer = io.BytesIO(file_bytes)
        xarray = xr.open_dataarray(file_buffer)
        return cls(xarray)

    def split(self, marker_value=2386, offset=None):
        """
        Split the scan into two scans based on the marker value
        :param marker_value: marker value
        :param offset: offset
        :return:
        """
        from .dataset import Dataset

        if "markers" not in self._xarr.coords:
            raise ValueError("The scan doesnt support markers")

        markers = np.where(self._xarr.coords["markers"] == marker_value)[0].tolist()
        num_traces = self.num_traces
        if offset:
            blocks_index = [(m - offset, m + offset) for m in markers]
        else:
            markers.extend([0, num_traces])
            markers = sorted(markers)
            blocks_index = [(start, stop) for start, stop in zip(markers, markers[1:])]
        blocks = {
            f"Block {i}": Scan(self._xarr[:, x:y].chunk("auto")) for i, (x, y) in enumerate(blocks_index)
        }
        return Dataset.from_dict(blocks)

    def subset(self, **kwargs):
        """
        Subset the scan object based on the coordinates
        :param kwargs: key value pairs of the coordinates
        :return:
        """
        coord_name, coord_index = kwargs.popitem()
        if coord_name not in self._xarr.dims and coord_name not in self._xarr.coords:
            raise ValueError(f"Invalid key: {coord_name}")
        return Scan(
            self._xarr.where(
                (self._xarr[coord_name] >= coord_index.start)
                & (self._xarr[coord_name] <= coord_index.stop),
                drop=True,
            )
        )

    def save(self, file_path: Union[str, Path, GenericPath], **kwargs):
        """
        Save the scan object to a file
        :param file_path: file path or GCP bucket
        :return:
        """
        file_path = GenericPath(file_path)
        if file_path.suffix == ".zarr":
            self._save_zarr(file_path, **kwargs)
        elif file_path.suffix == ".nc":
            self._save_netcdf(file_path, **kwargs)

    def _save_zarr(self, file_path: GenericPath, **kwargs):
        """
        Save the scan object to a zarr file
        :param file_path: file path or GCP bucket
        :return:
        """
        self._xarr.to_zarr(file_path, **kwargs)

    def _save_netcdf(self, file_path: GenericPath, **kwargs):
        """
        Save the scan object to a NetCDF file
        :param file_path: file path or GCP bucket
        :return:
        """

        # netcdf_file_bytes = self._xarr.to_netcdf()
        # file_path.write_bytes(netcdf_file_bytes)
        self._xarr.to_netcdf(file_path, **kwargs)

    def to_image(self,
              channel: int = 0,
              cmap: typing.Optional[str] = 'gray',
              stretch_func: StretchingFunction = None,
              stretch_func_args: dict = None,
              output_format: ImageOutputFormat = ImageOutputFormat.BASE64,
              quality: float =85,
              scale_factor: float=1.0,
              desired_chunk_mem = 100e6) -> typing.Union[str, PILImageType, np.ndarray]:
        """
        Convert the scan object into an image
        :param channel:
        :param cmap:
        :param stretch_func:
        :param stretch_func_args:
        :param output_format:
        :param quality:
        :param desired_chunk_mem:
        :return:
        """
        xarr = self._xarr = self._xarr.sel(channels=[channel])
        xarr = xarr.squeeze("channels")
        for dim in xarr.dims:
            xarr = xarr.dropna(dim=dim, how="all")

        return to_image(
            xarr,
            cmap=cmap,
            output_format=output_format,
            stretch_func=stretch_func,
            stretch_func_args=stretch_func_args,
            quality=quality,
            scale_factor=scale_factor,
            desired_chunk_mem=desired_chunk_mem
        )

    def plot(self, *args, **kwargs):
        """
        Plot the scan using the xarray plotting function
        :param args:
        :param kwargs:
        :return:
        """
        self._xarr.plot(*args, **kwargs)
        plt.show()

    def sel(self, **kwargs):
        """
        Select the item
        :param kwargs:
        :return:
        """
        return Scan(self._xarr.sel(**kwargs))

    def plot_coords(self):
        """
        Plot the scan on a map
        """
        from gprlibpy.widgets import MapViewer
        from gprlibpy.widgets.map_viewer.map_elements import Point, Polyline
        from PyQt6.QtWidgets import QApplication
        from PyQt6.QtCore import QSize
        import os
        import sys
        from dotenv import load_dotenv, find_dotenv

        for dim in self._xarr.dims:
            self._xarr = self._xarr.dropna(dim=dim, how="all")

        load_dotenv(find_dotenv())
        API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
        lat_values = self.xarr["lat"].values
        lng_values= self.xarr["lng"].values
        app = QApplication(sys.argv)
        gmap = MapViewer(api_key=API_KEY, provider="gmap")
        gmap.resize(QSize(800, 600))
        gmap.show()
        gmap.wait_for_map_ready()
        points = [Point(lat=lat, lng=lng) for lat, lng in zip(lat_values, lng_values)]
        gmap.add_polyline(
            Polyline(path=points,
                     geodesic=True,
                     strokeColor="red",
                     strokeOpacity=0.8,
                     strokeWeight=2),
                     center_to=True)
        gmap.set_zoom(22)
        app.exec()




