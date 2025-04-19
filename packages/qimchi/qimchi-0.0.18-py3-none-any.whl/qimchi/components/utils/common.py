import xarray as xr
from pathlib import Path
from dash.exceptions import PreventUpdate

# Local imports
from qimchi.state import load_state_from_disk
from qimchi.logger import logger


def _retry_reader(path, retries=3):
    """
    Utility function to retry reading a dataset

    Args:
        path (Path): Path to the dataset
        retries (int, optional): Number of retries. Defaults to 3.

    Returns:
        xr.Dataset: Loaded xarray dataset

    """
    for i in range(retries):
        try:
            ds = xr.load_dataset(path, engine="zarr")
            return ds
        except Exception as err:
            logger.warning(f"_retry_reader | Error reading: {path} | Err: {err}")
            logger.warning(f"_retry_reader | Retrying... {i + 1}/{retries}")

    logger.error(f"_retry_reader | Failed to read: {path} after {retries} retries")
    raise PreventUpdate


def read_data(sess_id: str, src: str) -> xr.Dataset:
    """
    Utility function to read data into a xarray.Dataset

    Args:
        sess_id (str): Session ID to load the state for
        src (str): Source of the read_data call. For debugging purposes.

    Returns:
        xr.Dataset: Loaded xarray dataset

    """
    _state = load_state_from_disk(sess_id)

    path = Path(_state.measurement_path)
    logger.debug(f"{src} -> read_data | Reading: {path}")

    if not path.is_dir() or not path.suffix == ".zarr":
        logger.warning(
            f"{src} -> read_data | Path is not a directory or not a zarr file: {path}"
        )
        raise PreventUpdate

    try:
        ds = xr.load_dataset(path, engine="zarr")
        logger.debug(f"{src} -> read_data | Reading done: {path}")
        return ds
    # Catch "FileNotFoundError: Unable to find group" and keep retrying
    except FileNotFoundError as err:
        logger.warning(
            f"{src} -> read_data | FileNotFoundError reading: {path} | err: {err}"
        )
        logger.warning(f"{src} -> read_data | Retrying...")
        ds = _retry_reader(path)
        return ds
    except KeyError as err:
        logger.warning(f"{src} -> read_data | KeyError reading: {path} | err: {err}")
        logger.warning(f"{src} -> read_data | Retrying...")
        ds = _retry_reader(path)
        return ds
    except Exception as err:
        logger.error(
            f"{src} -> read_data | Error reading: {path} | err: {err}", exc_info=True
        )
        raise PreventUpdate
