import typing

import numpy
import sklearn.base

import cvtda.dumping
from .process_iter import process_iter

def process_iter_dump(
    transformer: sklearn.base.TransformerMixin,
    data: numpy.ndarray,
    do_fit: bool,
    dump_name: typing.Optional[str] = None,
    *args,
    **kwargs
):
    if dump_name is None:
        return process_iter(transformer, data, do_fit, *args, **kwargs)
    
    if do_fit:
        transformer.fit(data, *args, **kwargs)
    return cvtda.dumping.dumper().execute(lambda: transformer.transform(data, *args, **kwargs), dump_name)
