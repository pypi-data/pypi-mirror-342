#!/usr/bin/env python
# coding=utf-8
"""
Author: Liu Kun && 16031215@qq.com
Date: 2024-09-17 17:12:47
LastEditors: Liu Kun && 16031215@qq.com
LastEditTime: 2024-12-13 19:11:08
FilePath: \\Python\\My_Funcs\\OAFuncs\\oafuncs\\oa_data.py
Description:
EditPlatform: vscode
ComputerInfo: XPS 15 9510
SystemInfo: Windows 11
Python Version: 3.11
"""


from typing import Any, List, Union

import numpy as np
import salem
import xarray as xr
from rich import print
from scipy.interpolate import griddata, interp1d

from oafuncs.oa_tool import PEx

__all__ = ["interp_along_dim", "interp_2d", "ensure_list", "mask_shapefile"]


def ensure_list(input_value: Any) -> List[str]:
    """
    Ensure the input is converted into a list.

    Args:
        input_value (Any): The input which can be a list, a string, or any other type.

    Returns:
        List[str]: A list containing the input or the string representation of the input.
    """
    if isinstance(input_value, list):
        return input_value
    elif isinstance(input_value, str):
        return [input_value]
    else:
        return [str(input_value)]


def interp_along_dim(
    target_coordinates: np.ndarray,
    source_coordinates: Union[np.ndarray, List[float]],
    source_data: np.ndarray,
    interpolation_axis: int = -1,
    interpolation_method: str = "linear",
    extrapolation_method: str = "linear",
) -> np.ndarray:
    """
    Perform interpolation and extrapolation along a specified dimension.

    Args:
        target_coordinates (np.ndarray): 1D array of target coordinate points.
        source_coordinates (Union[np.ndarray, List[float]]): Source coordinate points (1D or ND array).
        source_data (np.ndarray): Source data array to interpolate.
        interpolation_axis (int, optional): Axis to perform interpolation on. Defaults to -1.
        interpolation_method (str, optional): Interpolation method. Defaults to "linear".
        extrapolation_method (str, optional): Extrapolation method. Defaults to "linear".

    Returns:
        np.ndarray: Interpolated data array.

    Raises:
        ValueError: If input dimensions or shapes are invalid.

    Examples:
        >>> target_coordinates = np.array([1, 2, 3])
        >>> source_coordinates = np.array([0, 1, 2, 3])
        >>> source_data = np.array([10, 20, 30, 40])
        >>> result = interp_along_dim(target_coordinates, source_coordinates, source_data)
        >>> print(result)  # Expected output: [20.0, 30.0]
    """
    target_coordinates = np.asarray(target_coordinates)
    if target_coordinates.ndim != 1:
        raise ValueError("[red]target_coordinates must be a 1D array.[/red]")

    source_coordinates = np.asarray(source_coordinates)
    source_data = np.asarray(source_data)

    if source_data.ndim == 1 and source_coordinates.ndim == 1:
        if len(source_coordinates) != len(source_data):
            raise ValueError("[red]For 1D data, source_coordinates and source_data must have the same length.[/red]")

        interpolator = interp1d(source_coordinates, source_data, kind=interpolation_method, fill_value="extrapolate", bounds_error=False)
        return interpolator(target_coordinates)

    if source_coordinates.ndim == 1:
        shape = [1] * source_data.ndim
        shape[interpolation_axis] = source_coordinates.shape[0]
        source_coordinates = np.reshape(source_coordinates, shape)
        source_coordinates = np.broadcast_to(source_coordinates, source_data.shape)
    elif source_coordinates.shape != source_data.shape:
        raise ValueError("[red]source_coordinates and source_data must have the same shape.[/red]")

    def apply_interp_extrap(arr: np.ndarray) -> np.ndarray:
        xp = np.moveaxis(source_coordinates, interpolation_axis, 0)
        xp = xp[:, 0] if xp.ndim > 1 else xp
        arr = np.moveaxis(arr, interpolation_axis, 0)
        interpolator = interp1d(xp, arr, kind=interpolation_method, fill_value="extrapolate", bounds_error=False)
        interpolated = interpolator(target_coordinates)
        if extrapolation_method != interpolation_method:
            mask_extrap = (target_coordinates < xp.min()) | (target_coordinates > xp.max())
            if np.any(mask_extrap):
                extrap_interpolator = interp1d(xp, arr, kind=extrapolation_method, fill_value="extrapolate", bounds_error=False)
                interpolated[mask_extrap] = extrap_interpolator(target_coordinates[mask_extrap])
        return np.moveaxis(interpolated, 0, interpolation_axis)

    return np.apply_along_axis(apply_interp_extrap, interpolation_axis, source_data)


def _interp_single_worker(*args):
    """
    用于PEx并行的单slice插值worker，参数为(t, z, source_data, origin_points, target_points, interpolation_method, target_shape)
    """
    data_slice, origin_points, target_points, interpolation_method, target_shape = args

    return griddata(origin_points, data_slice.ravel(), target_points, method=interpolation_method).reshape(target_shape)


def interp_2d(
    target_x_coordinates: Union[np.ndarray, List[float]],
    target_y_coordinates: Union[np.ndarray, List[float]],
    source_x_coordinates: Union[np.ndarray, List[float]],
    source_y_coordinates: Union[np.ndarray, List[float]],
    source_data: np.ndarray,
    interpolation_method: str = "linear",
) -> np.ndarray:
    """
    Perform 2D interpolation on the last two dimensions of a multi-dimensional array.

    Args:
        target_x_coordinates (Union[np.ndarray, List[float]]): Target grid's x-coordinates.
        target_y_coordinates (Union[np.ndarray, List[float]]): Target grid's y-coordinates.
        source_x_coordinates (Union[np.ndarray, List[float]]): Original grid's x-coordinates.
        source_y_coordinates (Union[np.ndarray, List[float]]): Original grid's y-coordinates.
        source_data (np.ndarray): Multi-dimensional array with the last two dimensions as spatial.
        interpolation_method (str, optional): Interpolation method. Defaults to "linear".
        use_parallel (bool, optional): Enable parallel processing. Defaults to True.

    Returns:
        np.ndarray: Interpolated data array.

    Raises:
        ValueError: If input shapes are invalid.

    Examples:
        >>> target_x_coordinates = np.array([1, 2, 3])
        >>> target_y_coordinates = np.array([4, 5, 6])
        >>> source_x_coordinates = np.array([7, 8, 9])
        >>> source_y_coordinates = np.array([10, 11, 12])
        >>> source_data = np.random.rand(3, 3)
        >>> result = interp_2d(target_x_coordinates, target_y_coordinates, source_x_coordinates, source_y_coordinates, source_data)
        >>> print(result.shape)  # Expected output: (3, 3)
    """
    if len(target_y_coordinates.shape) == 1:
        target_x_coordinates, target_y_coordinates = np.meshgrid(target_x_coordinates, target_y_coordinates)
    if len(source_y_coordinates.shape) == 1:
        source_x_coordinates, source_y_coordinates = np.meshgrid(source_x_coordinates, source_y_coordinates)

    if source_x_coordinates.shape != source_data.shape[-2:] or source_y_coordinates.shape != source_data.shape[-2:]:
        raise ValueError("[red]Shape of source_data does not match shape of source_x_coordinates or source_y_coordinates.[/red]")

    target_points = np.column_stack((np.array(target_y_coordinates).ravel(), np.array(target_x_coordinates).ravel()))
    origin_points = np.column_stack((np.array(source_y_coordinates).ravel(), np.array(source_x_coordinates).ravel()))

    data_dims = len(source_data.shape)
    # Ensure source_data is 4D for consistent processing (t, z, y, x)
    if data_dims < 2:
        raise ValueError(f"[red]Source data must have at least 2 dimensions, but got {data_dims}.[/red]")
    elif data_dims > 4:
        # Or handle cases with more than 4 dimensions if necessary
        raise ValueError(f"[red]Source data has {data_dims} dimensions, but this function currently supports only up to 4.[/red]")

    # Reshape to 4D by adding leading dimensions of size 1 if needed
    num_dims_to_add = 4 - data_dims
    new_shape = (1,) * num_dims_to_add + source_data.shape
    new_src_data = source_data.reshape(new_shape)

    t, z, _, _ = new_src_data.shape

    paras = []
    target_shape = target_y_coordinates.shape
    for t_index in range(t):
        for z_index in range(z):
            paras.append((new_src_data[t_index, z_index], origin_points, target_points, interpolation_method, target_shape))
    
    with PEx() as excutor:
        result = excutor.run(_interp_single_worker, paras)
    excutor.shutdown()

    return np.squeeze(np.array(result))


def mask_shapefile(
    data_array: np.ndarray,
    longitudes: np.ndarray,
    latitudes: np.ndarray,
    shapefile_path: str,
) -> Union[xr.DataArray, None]:
    """
    Mask a 2D data array using a shapefile.

    Args:
        data_array (np.ndarray): 2D array of data to be masked.
        longitudes (np.ndarray): 1D array of longitudes.
        latitudes (np.ndarray): 1D array of latitudes.
        shapefile_path (str): Path to the shapefile used for masking.

    Returns:
        Union[xr.DataArray, None]: Masked xarray DataArray or None if an error occurs.

    Raises:
        FileNotFoundError: If the shapefile does not exist.
        ValueError: If the data dimensions do not match the coordinates.

    Examples:
        >>> data_array = np.random.rand(10, 10)
        >>> longitudes = np.linspace(-180, 180, 10)
        >>> latitudes = np.linspace(-90, 90, 10)
        >>> shapefile_path = "path/to/shapefile.shp"
        >>> masked_data = mask_shapefile(data_array, longitudes, latitudes, shapefile_path)
        >>> print(masked_data)  # Expected output: Masked DataArray

    """
    try:
        shp_f = salem.read_shapefile(shapefile_path)
        data_da = xr.DataArray(data_array, coords=[("latitude", latitudes), ("longitude", longitudes)])
        masked_data = data_da.salem.roi(shape=shp_f)
        return masked_data
    except Exception as e:
        print(f"[red]An error occurred: {e}[/red]")
        return None


if __name__ == "__main__":
    pass
