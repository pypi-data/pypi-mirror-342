import numpy
import sklearn.base

def process_iter(transformer: sklearn.base.TransformerMixin, data: numpy.ndarray, do_fit: bool, *args, **kwargs):
    if do_fit:
        transformer.fit(data, *args, **kwargs)
    return transformer.transform(data, *args, **kwargs)
