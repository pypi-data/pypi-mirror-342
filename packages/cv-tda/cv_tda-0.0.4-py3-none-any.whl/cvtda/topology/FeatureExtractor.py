import typing

import numpy
import gtda.images
import sklearn.base
import sklearn.preprocessing

from . import utils
import cvtda.logging
import cvtda.dumping
from .FiltrationsExtractor import FiltrationsExtractor
from .GreyscaleExtractor import GreyscaleExtractor
from .PointCloudsExtractor import PointCloudsExtractor
from .GeometryExtractor import GeometryExtractor


class FeatureExtractor(sklearn.base.TransformerMixin):
    def __init__(
        self,
        n_jobs: int = -1,
        reduced: bool = True,
        only_get_from_dump: bool = False,
        return_diagrams: bool = False,

        num_radial_filtrations: int = 4,
        binarizer_thresholds: typing.Optional[typing.List[float]] = None,
    ):
        self.fitted_ = False
        self.reduced_ = reduced
        self.return_diagrams_ = return_diagrams
        
        extractor_kwargs = { 'n_jobs': n_jobs, 'reduced': reduced, 'only_get_from_dump': only_get_from_dump }
        topological_extractor_kwargs = { **extractor_kwargs, 'return_diagrams': return_diagrams }

        self.inverter_ = gtda.images.Inverter()

        self.point_clouds_extractor_ = PointCloudsExtractor(**topological_extractor_kwargs)
        self.greyscale_extractor_ = GreyscaleExtractor(**topological_extractor_kwargs)
        self.inverted_greyscale_extractor_ = GreyscaleExtractor(**topological_extractor_kwargs)
        self.filtrations_extractor_ = FiltrationsExtractor(
            **topological_extractor_kwargs,
            binarizer_thresholds = binarizer_thresholds,
            num_radial_filtrations = num_radial_filtrations
        )
        self.geometry_extractor_ = GeometryExtractor(**extractor_kwargs)

        self.scaler_ = sklearn.preprocessing.StandardScaler(copy = False)

    def fit(self, images: numpy.ndarray, dump_name: typing.Optional[str] = None):
        self.process_(images, do_fit = True, dump_name = dump_name)
        self.fitted_ = True
        return self
    
    def transform(self, images: numpy.ndarray, dump_name: typing.Optional[str] = None):
        assert self.fitted_ is True, 'fit() must be called before transform()'
        return self.process_(images, do_fit = False, dump_name = dump_name)
    
    def fit_transform(self, images: numpy.ndarray, dump_name: typing.Optional[str] = None):
        return self.fit(images, dump_name = dump_name).transform(images, dump_name = dump_name)


    def process_(self, images: numpy.ndarray, do_fit: bool, dump_name: typing.Optional[str] = None):
        cvtda.logging.logger().print("Calculating inverted images")
        inverted_images = utils.process_iter(self.inverter_, images, do_fit = do_fit)

        point_clouds_dump = cvtda.dumping.dump_name_concat(dump_name, "point_clouds")
        greyscale_dump = cvtda.dumping.dump_name_concat(dump_name, "greyscale")
        inverted_greyscale_dump = cvtda.dumping.dump_name_concat(dump_name, "inverted_greyscale")
        filtrations_dump = cvtda.dumping.dump_name_concat(dump_name, "filtrations")
        geometry_dump = cvtda.dumping.dump_name_concat(dump_name, "geometry")

        results = []
        if not self.reduced_:
            results.append(utils.process_iter(self.point_clouds_extractor_, images, do_fit, point_clouds_dump))

        results.append(utils.process_iter(self.greyscale_extractor_, images, do_fit, greyscale_dump))
        results.append(utils.process_iter(self.inverted_greyscale_extractor_, inverted_images, do_fit, inverted_greyscale_dump))
        results.append(utils.process_iter(self.filtrations_extractor_, images, do_fit, filtrations_dump))
        
        if not self.return_diagrams_:
            results.append(utils.process_iter(self.geometry_extractor_, images, do_fit, geometry_dump))
        
        results = utils.hstack(results, not self.return_diagrams_)
        if self.return_diagrams_:
            cvtda.logging.logger().print("Diagrams requested. Returning diagrams.")
            return results
        
        cvtda.logging.logger().print("Applying StandardScaler.")
        return utils.process_iter(self.scaler_, results, do_fit)
