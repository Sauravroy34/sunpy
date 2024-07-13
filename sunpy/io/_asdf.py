from pathlib import Path
from collections import OrderedDict

import numpy as np

import asdf

from sunpy.io._header import FileHeader

__all__ = ["write", "read", "get_header", "get_keys_name"]

def write(fname, data, header, **kwargs):
    """
    Take ``(data, header)`` pairs and save it to an ASDF file.
    Parameters
    ----------
    fname : `str`
        File name, with extension.
    data : `numpy.ndarray`
        N-dimensional data array.
    header : `dict`
        A header dictionary.
    """
    map_name = Path(fname)
    map_name = map_name.name
    data = data.astype("float64")
    meta = dict(header)
    with asdf.AsdfFile() as af:
        af.tree={map_name:{"meta":meta,"data":data}}
        af.write_to(fname,**kwargs)


def read(fname,**kwargs):
    """
    Read an ASDF file.

    Parameters
    ----------
    filepath : `str`
        The ASDF file to be read.

    Returns
    -------
    `list`
        A list of "(data, header)" tuples.
    """

    with asdf.open(fname) as af:
        map_name = get_keys_name(fname)
        try:
            data = af[map_name]["data"].data
            data_array = np.asarray(data)
            meta_data= af[map_name]["meta"]
            meta_data = OrderedDict(meta_data)
            meta_data = FileHeader(meta_data)
            return [(data_array,meta_data)]
        except Exception:
            data = af[map_name].data
            meta_data = af[map_name].meta
            meta_data = OrderedDict(meta_data)
            meta_data = FileHeader(meta_data)
            return [(data,meta_data)]

def get_header(fname):
    """
    Read an ASDF file and return just the header(s).

    Parameters
    ----------
    fname : `str`
        The asdf file to be read.

    Returns
    -------
    `list`
        A list of `sunpy.io._header.FileHeader` headers.
    """
    with asdf.open(fname) as af:
        map_name = get_keys_name(fname)
        try:
            meta_data= af[map_name]["meta"]
            meta_data = OrderedDict(meta_data)
            meta_data = FileHeader(meta_data)
            return [meta_data]
        except Exception:
            meta_data = af[map_name].meta
            meta_data = OrderedDict(meta_data)
            meta_data = FileHeader(meta_data)
            return [meta_data]


def get_keys_name(fname):
    """
    returns the name of primary tree (excluding the info and history).
    Parameters
    ----------
    fname : `str`
        the asdf file to be read

    Returns
    -------
    `str`
        name of primary tree (excluding asdf and history).
    """
    with asdf.open(fname) as af:
        root_keys = af.tree.keys()
        main_data_keys = [key for key in root_keys if key not in ['asdf_library', 'history']]
        return main_data_keys[0]