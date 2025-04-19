import typing

from gprlibpy.core import Scan, Dataset
from lgopy.core import Block, apply_transform
import xarray as xr
import numpy as np
import dask.array as da
import inspect
import pandas as pd

import logging
logger = logging.getLogger(__name__)

def apply_transform2arr(transform: Block, xarr_in: xr.DataArray):
    """
    Apply a transform function to a Scan object.
    :param transform:
    :param xarr_in:
    :return:
    """
    block_extras = getattr(transform, "extras", {})
    is_multichannel = block_extras.get("multichannel", False)
    is_feature_extractor = block_extras.get("feature_extractor", False)

    ufunc = transform.call
    ufunc_signature = inspect.getfullargspec(ufunc)
    ufunc_annotations = ufunc_signature.annotations

    if not ufunc_annotations:
        raise NotImplementedError("Function annotations are missing. Expected annotations for input and return types.")

    arg_name, arg_signature = ufunc_annotations.popitem()
    ufunc_return = ufunc_annotations.pop("return", None)

    if arg_signature == xr.DataArray:
        return ufunc(xarr_in)

    if arg_signature != np.ndarray:
        raise NotImplementedError(f"Invalid input type. Expected np.ndarray but got {arg_signature}")

    # Compute if necessary to avoid dask errors
    if isinstance(xarr_in.data, da.Array):
        xarr_in = xarr_in.compute()

    # remove nan values
    for dim in xarr_in.dims:
        xarr_in = xarr_in.dropna(dim, how="all")


    apply_kwargs = {
        "vectorize": False if is_multichannel else True,
        "dask": "allowed" if not is_multichannel else None,
    }

    if is_multichannel:
        input_dims = output_dims = [["samples", "traces", "channels"]]
    else:
        input_dims, output_dims = [["samples", "traces"]], [["samples", "traces"]]

    if is_feature_extractor:
        return xr.apply_ufunc(ufunc,
                                 xarr_in,
                                 input_core_dims=input_dims,
                                 output_dtypes=[object], **apply_kwargs)


    xarr_out: xr.DataArray = xr.apply_ufunc(
        ufunc,
        xarr_in,
        input_core_dims=input_dims,
        output_core_dims=output_dims,
        keep_attrs= True,
        dask_gufunc_kwargs={"allow_rechunk": True} if not is_multichannel else None,
        **apply_kwargs
    )

    if not is_multichannel:
        xarr_out = xarr_out.transpose(..., "channels")

        # Convert NumPy output back to Dask
    if isinstance(xarr_out.data, np.ndarray):
        xarr_out.data = da.from_array(xarr_out.values)

    return xarr_out


def apply_transform2dataset(transform: Block, xarr_ds_in: xr.Dataset) -> xr.Dataset:
    """
    Apply a transform function to a Dataset object.
    :param transform:
    :param xarr_ds_in:
    :return:
    """

    def ufunc(xarr_in: xr.DataArray):
        transform_out = apply_transform2arr(transform, xarr_in)
        # Check if the output dimensions match the input dimensions
        if transform_out.dims != xarr_in.dims:
            return transform_out

        transform_out = transform_out.reindex_like(xarr_in, fill_value=np.nan)
        # Ensure coordinates are preserved
        for dim in xarr_in.dims:
            transform_out = transform_out.assign_coords({dim: xarr_in[dim]})
        # Ensure attributes are preserved
        transform_out.assign_attrs(xarr_in.attrs)
        return transform_out

    return xarr_ds_in.map(ufunc)

# Register the function as a specialized implementation for `apply_transform`
@apply_transform.register
def _(x: Scan, transform: Block):
    """
    Applies a transformation to a Scan object and processes the output based on
    whether the transformation is a feature extractor and whether it handles multiple channels.

    Args:
        x (Scan): The input scan object containing data.
        transform (Block): The transformation block to be applied.

    Returns:
        If the transformation is a feature extractor:
            - Returns a DataFrame if it's multichannel.
            - Returns a normalized DataFrame if it's a single-channel feature extractor.
        Otherwise:
            - Returns a transformed Scan object.
    """

    is_passthrough_block = getattr(transform, "passthroughBlock", False)
    if is_passthrough_block:
        return transform.call(x.xarr)

    transform_out = apply_transform2arr(transform, x._xarr)

    # Retrieve additional attributes from the transformation block, if any
    block_extras = getattr(transform, "extras", {})

    # Determine if the transform is a feature extractor
    is_feature_extractor = block_extras.get("feature_extractor", False)

    # Determine if the transform processes multiple channels
    is_multichannel = block_extras.get("multichannel", False)

    # If the transform is a feature extractor, process the output accordingly
    if is_feature_extractor:
        if is_multichannel:
            # Convert the transformed data to a pandas DataFrame with the scan name as the index
            df = pd.DataFrame(index=[x.name], data=transform_out.to_dict()["data"])
            return df

        # Convert the transformation output to a pandas DataFrame or Series
        df = transform_out.to_pandas()

        # Ensure the DataFrame has the correct format (convert Series to DataFrame if needed)
        if isinstance(df, pd.Series):
            df = df.to_frame().T  # Convert to DataFrame and transpose to have features as columns

        # Reshape the DataFrame: stack and reset index to organize scan, channel, and features
        df = df.stack().reset_index()

        # Rename columns to match expected format
        df.columns = ["scan", "channel", "features"]

        # Convert the DataFrame into a list of dictionaries
        df = df.to_dict(orient="records")

        # Normalize the dictionary structure into a flattened DataFrame
        df = pd.json_normalize(df)

        return df  # Return the final processed DataFrame

    # If the transform is not a feature extractor, return a new Scan object with transformed data
    return Scan(transform_out)


# Register the function as a specialized implementation for `apply_transform`
@apply_transform.register
def _(x: Dataset, transform: Block):
    """
    Applies a transformation to a Dataset object and processes the output
    based on whether the transformation is a feature extractor.

    Args:
        x (Dataset): The input dataset containing multiple scans.
        transform (Block): The transformation block to be applied.

    Returns:
        If the transformation is a feature extractor:
            - Returns a structured and normalized DataFrame.
        Otherwise:
            - Returns a transformed Dataset object.
    """
    is_passthrough_block = getattr(transform, "passthroughBlock", False)
    if is_passthrough_block:
        return transform.call(x.xarr_ds)

    # Apply the transformation to the dataset's internal xarray dataset representation
    transform_out = apply_transform2dataset(transform, x.xarr_ds)

    # Retrieve additional attributes from the transformation block, if any
    block_extras = getattr(transform, "extras", {})

    # Determine if the transform is a feature extractor
    is_feature_extractor = block_extras.get("feature_extractor", False)

    # If the transform is a feature extractor, process the output accordingly
    if is_feature_extractor:
        # Convert the transformation output to a pandas DataFrame or Series
        df = transform_out.to_pandas()

        # Ensure the DataFrame has the correct format (convert Series to DataFrame if needed)
        if isinstance(df, pd.Series):
            df = df.to_frame().T  # Convert to DataFrame and transpose to have features as columns

        # Reshape the DataFrame: stack and reset index to organize channel, scan, and features
        df = df.stack().reset_index()

        # Rename columns to match expected format
        df.columns = ["channel", "scan", "features"]

        # Convert the DataFrame into a list of dictionaries
        df = df.to_dict(orient="records")

        # Normalize the dictionary structure into a flattened DataFrame
        df = pd.json_normalize(df)

        return df  # Return the final processed DataFrame

    # If the transform is not a feature extractor, return a new Dataset object with transformed data
    return Dataset(transform_out)

