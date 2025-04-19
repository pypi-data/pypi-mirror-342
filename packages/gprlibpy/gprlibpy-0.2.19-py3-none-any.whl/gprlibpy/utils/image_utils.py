import base64
import logging
import typing
from enum import Enum, auto
import io
import xarray as xr
import dask.array as da

import cv2
import graphviz
import numpy as np
from PIL import Image
from dask import optimize
from matplotlib import pyplot as plt

logger = logging.getLogger(__name__)

class ImageOutputFormat(Enum):
    """
    This class provides a set of image output formats
    """

    PIL = auto()
    BASE64 = auto()
    NUMPY = auto()

class StretchingFunction(Enum):
    """
    This enum provides a set of stretching functions
    """
    STDEV_CLIPPED = auto()



def timeit(func):
    """
    Decorator to measure the execution time of a function.
    """

    def wrapper(*args, **kwargs):
        import time

        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logger.info(f"Execution time: {end_time - start_time:.2f} seconds")
        return result

    return wrapper

def calculate_optimal_chunks(data_shape, dtype=np.float64, desired_chunk_mem=100e6):
    """
    Calculate optimal chunk sizes for a Dask array.

    Parameters:
    - data_shape (tuple): Shape of the array (e.g., (10000, 10000)).
    - dtype (data-type): NumPy data type (e.g., np.float64). Default is np.float64.
    - desired_chunk_mem (float): Desired chunk size in bytes. Default is 100MB.

    Returns:
    - tuple: Optimal chunk sizes for each dimension.
    """
    try:
        # Calculate the size of one element in bytes
        element_size = np.dtype(dtype).itemsize
        # Total number of elements in the array
        total_elements = np.prod(data_shape)
        # Total size of the array in bytes
        total_size = total_elements * element_size
        # Number of chunks desired
        num_chunks = total_size / desired_chunk_mem
        # Calculate the chunk size for each dimension
        chunk_size = int(np.ceil(np.power(total_elements / num_chunks, 1 / len(data_shape))))
        # Create the chunk shape
        chunk_shape = tuple(min(dim, chunk_size) for dim in data_shape)
        return chunk_shape
    except Exception as e:
        logger.error(f"Error calculating optimal chunks: {e}")
        return "auto"

def stdev_clipped_normalization(array: da.Array, num_stdev: float):
    """
    Stretch an array based on the number of standard deviations using dask.array
    """
    # scale values first to 0-1 to reduce memory usage
    array = array.astype(da.float32)
    array = da.nan_to_num(array)
    data_stdev = da.std(array)
    data_mean = da.mean(array)
    data_max_new = data_mean + num_stdev * data_stdev
    data_min_new = data_mean - num_stdev * data_stdev
    array = da.clip(array, data_min_new, data_max_new)
    data_max = da.max(array)
    data_min = da.min(array)
    data_range = data_max - data_min

    array = (array - data_min) / data_range
    return array


@timeit
def to_image(xarr: xr.DataArray,
             cmap: typing.Optional[str] = 'gray',
             stretch_func: StretchingFunction = None,
             stretch_func_args: dict = None,
             output_format: ImageOutputFormat = ImageOutputFormat.BASE64,
             quality: float = 85,
             scale_factor: float = 1.0,
             desired_chunk_mem: float = 100e6) -> typing.Union[str, Image.Image, np.ndarray]:
    """
    Converts a large 3D GPR array (samples, traces, channels) into a Base64-encoded image using Dask.

    Parameters:
    - xarr (xr.DataArray): 3D GPR array (samples, traces, channels)
    - cmap (Optional[str]): Matplotlib colormap name. Default is 'gray'. If None, no colormap is applied.
    - stretch_func (StretchingFunction): Stretching function. Default is None.
    - stretch_func_args (dict): Stretching function arguments. Default is None.
    - output_format (ImageOutputFormat): Output format. Default is ImageOutputFormat.BASE64.
    - quality (int): Image quality (0-100). Default is 85.
    - scale_factor (float): Scale factor for resizing the image. Default is 1.0.
    - desired_chunk_mem (float): Desired chunk size in bytes. Default is 100MB.

    Returns:
        Union[str, Image.Image, np.ndarray]: Encoded image in the requested format.
    """
    xarr = xarr.data  # Extract Dask array from xarray
    if not isinstance(xarr, da.Array):
        xarr = da.from_array(xarr, chunks="auto")

    stretch_funcs = {
        StretchingFunction.STDEV_CLIPPED: stdev_clipped_normalization
    }

    data_shape = xarr.shape
    dtype = xarr.dtype
    optimal_chunks = calculate_optimal_chunks(data_shape, dtype, desired_chunk_mem)
    xarr = xarr.rechunk(optimal_chunks)

    stretch_func = stretch_funcs.get(stretch_func, None)
    if stretch_func is not None:
        xarr = stretch_func(xarr, **(stretch_func_args or {}))

    # Step 3: Apply colormap in parallel (only if cmap is provided)
    def apply_colormap(chunk_arr):
        if cmap:
            cmap_func = plt.get_cmap(cmap)
            chunk_arr = cmap_func(chunk_arr)
            chunk_arr = np.uint8(chunk_arr * 255)
        return chunk_arr

    if cmap:
        dask_colored = xarr.map_blocks(apply_colormap, dtype=np.uint8, new_axis=2)
        dask_colored = optimize(dask_colored)[0]
        final_image = dask_colored.compute()
    else:
        xarr = (xarr - xarr.min()) / (xarr.max() - xarr.min()) * 255
        xarr = xarr.astype(np.uint8)
        final_image = xarr.compute()

    pil_img = Image.fromarray(final_image)
    pil_img = pil_img.resize((int(pil_img.width * scale_factor), int(pil_img.height * scale_factor)))

    if output_format == ImageOutputFormat.NUMPY:
        return np.asarray(pil_img)
    elif output_format == ImageOutputFormat.BASE64:
        with io.BytesIO() as buffered:
            pil_img.save(buffered, format="PNG", quality=quality)
            base64_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        return base64_str
    return pil_img

# @timeit
# def to_image(xarr: xr.DataArray,
#                        cmap: typing.Optional[str] = 'gray',
#                        stretch_func: typing.Optional[StretchingFunction] = None,
#                        stretch_func_args: typing.Optional[dict] = None,
#                        output_format: ImageOutputFormat = ImageOutputFormat.BASE64,
#                        quality: int = 85, # Quality often applies more to JPEG
#                        scale_factor: float = 1.0,
#                        desired_chunk_mem: float = 100e6,
#                        resampling_method = Image.Resampling.LANCZOS
#                        ) -> typing.Union[str, Image.Image, np.ndarray]:
#     """
#     Converts a large ND Dask/NumPy array into an image, optimized for speed.
#     Assumes the first two dimensions are spatial (height, width) for imaging.
#
#     Parameters:
#     - xarr (xr.DataArray): Input array (potentially ND, assumed HxWxC... or HxW)
#     - cmap (Optional[str]): Matplotlib colormap name. Default 'gray'. If None, uses grayscale.
#     - stretch_func (Optional[StretchingFunction]): Stretching function enum member. Default None.
#     - stretch_func_args (dict): Stretching function arguments. Default None.
#     - output_format (ImageOutputFormat): Output format. Default ImageOutputFormat.BASE64.
#     - quality (int): Image quality (0-100), mainly for lossy formats like JPEG. Affects PNG compression level.
#     - scale_factor (float): Scale factor for resizing the image. Default 1.0.
#     - desired_chunk_mem (float): Desired chunk size in bytes. Default 100MB.
#     - resampling_method: PIL resampling method for final resize (e.g., Image.Resampling.NEAREST, .BILINEAR, .LANCZOS).
#
#     Returns:
#         Union[str, Image.Image, np.ndarray]: Encoded image in the requested format.
#     """
#     if not isinstance(xarr, xr.DataArray):
#         raise TypeError("Input must be an xarray.DataArray")
#
#     # --- 1. Initial Setup ---
#     dask_arr = xarr.data # Extract Dask array or NumPy array
#     original_shape = dask_arr.shape
#     original_dtype = dask_arr.dtype
#
#     if len(original_shape) < 2:
#         raise ValueError("Input array must have at least 2 dimensions (Height, Width)")
#
#     # Ensure it's a Dask array for parallel processing
#     if not isinstance(dask_arr, da.Array):
#         # Use calculate_optimal_chunks logic also for initial chunking if coming from numpy
#         initial_chunks = calculate_optimal_chunks(original_shape, original_dtype, desired_chunk_mem)
#         dask_arr = da.from_array(dask_arr, chunks=initial_chunks)
#     else:
#         # Rechunk if necessary based on desired memory
#         optimal_chunks = calculate_optimal_chunks(original_shape, original_dtype, desired_chunk_mem)
#         if dask_arr.chunksize != optimal_chunks:
#             # print(f"Rechunking from {dask_arr.chunksize} to {optimal_chunks}") # Debugging
#             dask_arr = dask_arr.rechunk(optimal_chunks)
#
#     # --- 2. Apply Stretching (if any) ---
#     stretch_funcs = {
#         StretchingFunction.STDEV_CLIPPED: stdev_clipped_normalization
#         # Add other functions here
#     }
#     if stretch_func is not None:
#         selected_stretch_func = stretch_funcs.get(stretch_func)
#         if selected_stretch_func:
#             # Pass arguments, ensure stretch func handles dask array
#             dask_arr = selected_stretch_func(dask_arr, **(stretch_func_args or {}))
#         else:
#             print(f"Warning: Stretching function '{stretch_func}' not found or implemented.")
#
#     # --- 3. Downsample with Dask Coarsening (if scale_factor < 1.0) ---
#     # Perform coarse downsampling *before* normalization/colormap for massive speedup
#     effective_scale_factor = scale_factor
#     target_height = int(original_shape[0] * scale_factor)
#     target_width = int(original_shape[1] * scale_factor)
#
#     if scale_factor < 1.0 and target_height > 0 and target_width > 0 :
#         # Calculate integer coarsening factors (must be > 0)
#         # Using ceiling ensures we don't coarsen *more* than needed
#         ch = max(1, int(np.ceil(original_shape[0] / target_height)))
#         cw = max(1, int(np.ceil(original_shape[1] / target_width)))
#
#         if ch > 1 or cw > 1:
#             coarsen_factors = {0: ch, 1: cw}
#             # Coarsen remaining dims by 1 (no change)
#             for i in range(2, dask_arr.ndim):
#                  coarsen_factors[i] = 1
#
#             # print(f"Coarsening by factors: H={ch}, W={cw}") # Debugging
#             # Use mean for aggregation, allow degenerate axes if factor > dim size
#             dask_arr = dask_arr.coarsen(coarsen_factors, trim_excess=True, boundary='trim').mean(keepdims=False) # Check keepdims based on need
#             # print(f"Shape after coarsening: {dask_arr.shape}") # Debugging
#
#             # Update effective scale factor for the *final* PIL resize,
#             # as coarsening is approximate.
#             current_shape = dask_arr.shape # Shape after coarsening
#             # Calculate scale needed to get from coarsened size to final target size
#             scale_h = target_height / current_shape[0]
#             scale_w = target_width / current_shape[1]
#             # We'll use these factors in the final PIL resize step
#             # For simplicity in PIL resize, we often use a single factor.
#             # Using the average or min might be reasonable. Let's use average:
#             effective_scale_factor = (scale_h + scale_w) / 2.0
#             # Ensure the final PIL resize doesn't upscale significantly if coarsening was aggressive
#             if effective_scale_factor > 1.5: # Heuristic threshold
#                  print(f"Warning: Coarsening resulted in significant intermediate downsampling. Final resize might be blurry.")
#                  # Cap the final resize to avoid excessive upscaling from the coarsened version
#                  # effective_scale_factor = 1.0 # Or recalculate target size based on current_shape
#
#         else:
#             # No coarsening needed if factors are 1
#             effective_scale_factor = scale_factor
#
#
#     # --- 4. Normalize Data Range and Apply Colormap (using LUT) ---
#     # Compute min/max *once* after stretching and potential coarsening
#     dmin, dmax = da.compute(dask_arr.min(), dask_arr.max())
#
#     # Avoid division by zero if data is flat
#     if dmax == dmin:
#         # Handle flat data: map everything to the middle gray or the start of the cmap
#         norm_factor = 0.0
#         offset = dmin # Doesn't matter much, but avoids NaN potential
#         # Set dask_arr to a constant value (e.g., 128 for uint8)
#         # Need to be careful with dtype here. Let's do it during map_blocks.
#         print("Warning: Data range is zero (flat data).")
#     else:
#         norm_factor = 255.0 / (dmax - dmin)
#         offset = dmin
#
#     # Prepare Colormap LUT or Grayscale mapping
#     if cmap:
#         try:
#             cmap_func = plt.get_cmap(cmap)
#             # Create a lookup table (LUT) from the colormap
#             lut = cmap_func(np.linspace(0, 1, 256))  # Get RGBA values (0.0-1.0)
#             lut_uint8 = (lut * 255).astype(np.uint8) # Convert to uint8 RGBA
#
#             def apply_lut_chunk(chunk, offset, norm_factor, lut):
#                 if norm_factor == 0.0: # Handle flat data case
#                     # Map to the middle color of the LUT
#                     scaled_chunk = np.full(chunk.shape, 128, dtype=np.uint8)
#                 else:
#                     # Scale chunk to 0-255
#                     scaled_chunk = (chunk - offset) * norm_factor
#                     # Clip, convert to uint8 (indices for LUT)
#                     scaled_chunk = np.clip(scaled_chunk, 0, 255).astype(np.uint8)
#                 # Apply LUT
#                 return lut[scaled_chunk]
#
#             # Define output chunks: same spatial dims, last dim is 4 (RGBA)
#             output_chunks = dask_arr.chunks[:-1] + (4,) if dask_arr.ndim > 1 else (4,) # Handle 1D input edge case? Assumes input >= 2D
#             if dask_arr.ndim == 2: # If input was 2D (H, W)
#                  output_chunks = dask_arr.chunks + (4,)
#
#
#             # Map blocks using the LUT
#             img_dask = dask_arr.map_blocks(
#                 apply_lut_chunk,
#                 offset=offset,
#                 norm_factor=norm_factor,
#                 lut=lut_uint8,
#                 dtype=np.uint8,
#                 chunks=output_chunks, # Specify output chunk shape
#                 new_axis=dask_arr.ndim # Add new axis for color dimension if input was 2D
#             )
#             if dask_arr.ndim == 2: # Correct map_blocks call for 2D->3D
#                  img_dask = dask_arr.map_blocks(
#                     apply_lut_chunk,
#                     offset=offset,
#                     norm_factor=norm_factor,
#                     lut=lut_uint8,
#                     dtype=np.uint8,
#                     # chunks need care here if input chunks are large
#                     # Let dask infer output chunks if possible, or specify carefully
#                     # chunks=dask_arr.chunks + (4,), # This might be too simplistic
#                     meta=np.empty((0,0,4), dtype=np.uint8) # Provide meta example
#                  )
#                  # Dask might add the new axis automatically sometimes. Test this.
#                  # Let's try letting dask infer chunks and check ndim later
#                  img_dask = dask_arr.map_blocks(
#                      apply_lut_chunk,
#                      offset=offset,
#                      norm_factor=norm_factor,
#                      lut=lut_uint8,
#                      dtype=np.uint8,
#                      meta=np.empty((0,0,4), dtype=np.uint8) # Provide meta example
#                      )
#
#
#         except ValueError:
#             print(f"Warning: Colormap '{cmap}' not found. Falling back to grayscale.")
#             cmap = None # Force grayscale path
#
#     if not cmap: # Grayscale path (either requested or fallback)
#         def scale_to_gray_chunk(chunk, offset, norm_factor):
#              if norm_factor == 0.0: # Handle flat data case
#                  return np.full(chunk.shape, 128, dtype=np.uint8)
#              else:
#                 scaled_chunk = (chunk - offset) * norm_factor
#                 return np.clip(scaled_chunk, 0, 255).astype(np.uint8)
#
#         img_dask = dask_arr.map_blocks(
#             scale_to_gray_chunk,
#             offset=offset,
#             norm_factor=norm_factor,
#             dtype=np.uint8
#             # Output chunks are same as input for grayscale
#         )
#         # Ensure output is treated as 2D for image conversion later if input was >2D
#         if img_dask.ndim > 2:
#              # This assumes grayscale output from ND input means taking the first slice/channel
#              # Adjust if averaging or other reduction is needed
#              print(f"Warning: Input array had {dask_arr.ndim} dimensions. Taking slice [:, :, 0] for grayscale image.")
#              img_dask = img_dask[..., 0]
#
#
#     # --- 5. Compute the (Potentially Downsampled) Image Data ---
#     # This is now the main computation step, operating on reduced data if coarsened
#     # print(f"Computing Dask array of shape {img_dask.shape} and chunks {img_dask.chunksize}...") # Debugging
#     computed_image_data = img_dask.compute()
#     # print(f"Computed NumPy array shape: {computed_image_data.shape}, dtype: {computed_image_data.dtype}") # Debugging
#
#
#     # --- 6. Final Resizing with PIL ---
#     # Convert computed data (potentially RGBA or Grayscale) to PIL Image
#     try:
#         # Handle potential extra dimensions if input was > 3D and colormapped
#         if computed_image_data.ndim == 3 and computed_image_data.shape[2] not in (3, 4): # e.g. HxWxOther
#              print(f"Warning: Computed data is 3D but not RGB/RGBA ({computed_image_data.shape}). Taking slice [:, :, 0].")
#              final_image_array = computed_image_data[:, :, 0]
#         elif computed_image_data.ndim > 3:
#              print(f"Warning: Computed data has {computed_image_data.ndim} dimensions ({computed_image_data.shape}). Taking slice [:, :, 0, ...].")
#              final_image_array = computed_image_data[:, :, 0] # Or adapt based on expected structure
#         else:
#              final_image_array = computed_image_data
#
#         pil_img = Image.fromarray(final_image_array)
#     except Exception as e:
#         print(f"Error converting computed array (shape: {computed_image_data.shape}, dtype: {computed_image_data.dtype}) to PIL Image: {e}")
#         raise
#
#     # Calculate the *final* target size based on the *original* shape
#     # Use the effective_scale_factor if coarsening was done, otherwise original scale_factor
#     final_target_height = int(original_shape[0] * scale_factor)
#     final_target_width = int(original_shape[1] * scale_factor)
#
#     # Only resize if needed and target size is valid
#     if (pil_img.height != final_target_height or pil_img.width != final_target_width) \
#        and final_target_height > 0 and final_target_width > 0:
#         # print(f"Resizing PIL image from {pil_img.size} to {(final_target_width, final_target_height)} using {resampling_method}") # Debugging
#         try:
#             pil_img = pil_img.resize((final_target_width, final_target_height), resample=resampling_method)
#         except ValueError as e:
#             print(f"Error during PIL resize: {e}. Check target dimensions: ({final_target_width}, {final_target_height})")
#             # Decide how to handle: return unresized, raise error?
#             # Returning unresized might be safest if target dims are invalid (e.g., zero)
#             print("Returning image without final resize due to error.")
#
#
#     # --- 7. Format Output ---
#     if output_format == ImageOutputFormat.NUMPY:
#         # Convert back to NumPy array after potential resize
#         return np.asarray(pil_img)
#     elif output_format == ImageOutputFormat.BASE64:
#         with io.BytesIO() as buffered:
#             # Use imageio for potentially faster PNG encoding
#             # quality affects compression for PNG, 0=fastest, 9=best compression
#             pil_compression = int(round(9 - (quality / 100.0) * 9)) # Map 0-100 to 9-0
#             iio.imwrite(buffered, np.asarray(pil_img), format='PNG', compression=pil_compression)
#             # Fallback to PIL save if needed:
#             # pil_img.save(buffered, format="PNG", optimize=True, compress_level=pil_compression) # optimize might help slightly
#             base64_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
#         return base64_str
#     elif output_format == ImageOutputFormat.PIL:
#         return pil_img
#     else:
#         raise ValueError(f"Unsupported output format: {output_format}")


def array2rgb(data_arr: np.ndarray):
    """
    Convert a numpy array to a RGB image
    :param data_arr:
    :return:
    """
    data_arr = data_arr.astype("float")
    data_arr = cv2.normalize(data_arr, None, 0.0, 255.0, cv2.NORM_MINMAX)
    data_arr = data_arr.astype(np.uint8)
    data_arr = cv2.cvtColor(data_arr, cv2.COLOR_GRAY2RGB)
    return Image.fromarray(data_arr, "RGB")

def scale(x, out_range=(-1, 1), axis=None):
    """
    Scale the data to a given range
    :param x: input data
    :param out_range: scale to this range
    :param axis: scale along this axis
    :return: scaled data
    """
    in_range = np.min(x, axis), np.max(x, axis)
    y = (x - (in_range[1] + in_range[0]) / 2) / (in_range[1] - in_range[0])
    return y * (out_range[1] - out_range[0]) + (out_range[1] + out_range[0]) / 2

def normalize(data_arr):
    """ "
    Normalize the data array
    :param data_arr: input data array
    :return: normalized data array
    """
    if data_arr.dtype == np.uint8:
        data_arr = data_arr.astype(np.float32) / 255.0
    else:
        data_arr = data_arr.astype(np.float32)
        data_arr = cv2.normalize(data_arr, None, 0.0, 1.0, cv2.NORM_MINMAX)
    return data_arr


def dgraph2image(d: graphviz.Digraph):
    """
    Convert a graphviz digraph to an image
    :param d:
    :return:
    """
    graph_stream = bytearray(d.pipe())
    graph_numpy = np.asarray(graph_stream, dtype=np.uint8)
    graph_image = cv2.imdecode(graph_numpy, cv2.IMREAD_COLOR)
    return graph_image


def stdev_clipped_normalization(array, num_stdev):
    """
    Stretch an array based on the number of standard deviations
    """
    array = array.astype(np.float32)
    data_stdev = np.std(array)
    data_mean = np.mean(array)
    data_max_new = data_mean + num_stdev * data_stdev
    data_min_new = data_mean - num_stdev * data_stdev
    array[array > data_max_new] = data_max_new
    array[array < data_min_new] = data_min_new
    data_max = np.max(array)
    data_min = np.min(array)
    data_range = data_max - data_min
    array = (array - data_min) / data_range
    return array

def fft2(data_arr):
    """
    This function is used to calculate the 2D FFT of an image
    :param data_arr: 2D array
    """
    data_fk_arr = np.fft.fft2(data_arr)
    data_fk_arr = np.fft.fftshift(data_fk_arr)
    data_fk_arr = abs(data_fk_arr)
    return data_fk_arr.astype(np.float32)


def ifft2(data_arr):
    """
    This function is used to calculate the 2D IFFT of an image
    :param data_arr: 2D array
    """
    data_fk_arr = np.fft.ifftshift(data_arr)
    data_fk_arr = np.fft.ifft2(data_fk_arr)
    data_fk_arr = abs(data_fk_arr)
    return data_fk_arr.astype(np.float32)
