import typing

import numpy
import itertools
import gtda.images
import sklearn.base
import gtda.homology

import cvtda.utils
import cvtda.logging

from . import utils
import cvtda.dumping
from .interface import TopologicalExtractor


class FiltrationExtractor(TopologicalExtractor):
    def __init__(
        self,
        filtration_class,
        filtation_kwargs: dict,
        binarizer_threshold: float,

        n_jobs: int = -1,
        reduced: bool = True,
        only_get_from_dump: bool = False,
        return_diagrams: bool = False,
        **kwargs
    ):
        super().__init__(
            supports_rgb = False,
            n_jobs = n_jobs,
            reduced = reduced,
            only_get_from_dump = only_get_from_dump,
            return_diagrams = return_diagrams,
            filtration_class = filtration_class,
            filtation_kwargs = filtation_kwargs,
            binarizer_threshold = binarizer_threshold,
            **kwargs
        )

        self.binarizer_ = gtda.images.Binarizer(threshold = binarizer_threshold, n_jobs = self.n_jobs_)
        self.filtration_ = filtration_class(**filtation_kwargs, n_jobs = self.n_jobs_)
        self.persistence_ = gtda.homology.CubicalPersistence(homology_dimensions = [ 0, 1 ], n_jobs = self.n_jobs_)


    def get_diagrams_(self, images: numpy.ndarray, do_fit: bool, dump_name: typing.Optional[str] = None):
        cvtda.logging.logger().print(f"FiltrationExtractor: processing {dump_name}, do_fit = {do_fit}, filtration = {self.filtration_}")
        
        bin_images = utils.process_iter(self.binarizer_, images, do_fit)
        assert bin_images.shape == images.shape

        filtrations = utils.process_iter(self.filtration_, bin_images, do_fit)
        assert filtrations.shape == images.shape

        return utils.process_iter_dump(self.persistence_, filtrations, do_fit, self.diagrams_dump_(dump_name))


class FiltrationsExtractor(sklearn.base.TransformerMixin):
    def __init__(
        self,

        n_jobs: int = -1,
        reduced: bool = True,
        only_get_from_dump: bool = False,
        return_diagrams: bool = False,

        binarizer_thresholds: typing.Optional[typing.List[float]] = None,
        height_filtration_directions: typing.Iterable[typing.Tuple[float, float]] = [
            [ -1, -1 ], [ 1, 1 ], [ 1, -1 ], [ -1, 1 ],
            [ 0, -1 ], [ 0, 1 ], [ -1, 0 ], [ 1, 0 ]
        ],
        num_radial_filtrations: int = 4,
        density_filtration_radiuses: typing.Iterable[int] = [ 1, 3 ],
    ):
        if not binarizer_thresholds:
            if reduced:
                binarizer_thresholds = [ 0.2, 0.4, 0.6 ]
            else:
                binarizer_thresholds = [ 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9 ]

        self.fitted_ = False
        self.reduced_ = reduced
        self.return_diagrams_ = return_diagrams
        self.filtrations_kwargs_ = {
            'n_jobs': n_jobs,
            'reduced': reduced,
            'only_get_from_dump': only_get_from_dump,
            'return_diagrams': return_diagrams
        }

        self.binarizer_thresholds_ = binarizer_thresholds
        self.height_filtration_directions_ = height_filtration_directions
        self.num_radial_filtrations_ = num_radial_filtrations
        self.density_filtration_radiuses_ = density_filtration_radiuses

        self.filtration_extractors_: typing.List[typing.Tuple[FiltrationExtractor, str]] = []


    def fit(self, images: numpy.ndarray, dump_name: typing.Optional[str] = None):
        assert len(images.shape) >= 3, f'{len(images.shape) - 1}d images are not supported'
        cvtda.logging.logger().print("Fitting filtrations")

        self._fill_filtrations(images.shape[1], images.shape[2])
        for i, (filtration_extractor, name) in enumerate(self.filtration_extractors_):
            cvtda.logging.logger().print(f"Fitting filtration {i + 1}/{len(self.filtration_extractors_)}: {name}")
            filtration_extractor.fit(images, cvtda.dumping.dump_name_concat(dump_name, name))
        self.fitted_ = True
        return self
    
    def transform(self, images: numpy.ndarray, dump_name: typing.Optional[str] = None) -> numpy.ndarray:
        assert self.fitted_ is True, 'fit() must be called before transform()'
        cvtda.logging.logger().print("Applying filtrations")
        
        outputs = [ ]
        for i, (filtration_extractor, name) in enumerate(self.filtration_extractors_):
            cvtda.logging.logger().print(f"Applying filtration {i + 1}/{len(self.filtration_extractors_)}: {name}")
            outputs.append(filtration_extractor.transform(images, cvtda.dumping.dump_name_concat(dump_name, name)))
        return utils.hstack(outputs, not self.return_diagrams_)
    
    def fit_transform(self, images: numpy.ndarray, dump_name: typing.Optional[str] = None) -> numpy.ndarray:
        return self.fit(images, dump_name = dump_name).transform(images, dump_name = dump_name)


    def _fill_filtrations(self, width: int, height: int):
        radial_x = cvtda.utils.spread_points(width, self.num_radial_filtrations_)
        radial_y = cvtda.utils.spread_points(height, self.num_radial_filtrations_)
        cvtda.logging.logger().print(f"Calculated radial centers for images of size {width}x{height}: {radial_x}x{radial_y}")

        self.filtration_extractors_ = [ ]
        for binarizer_threshold in self.binarizer_thresholds_:
            self._add_height_filtrations(binarizer_threshold)
            self._add_radial_filtrations(binarizer_threshold, radial_x, radial_y)
            self._add_dilation_filtrations(binarizer_threshold)
            self._add_erosion_filtrations(binarizer_threshold)
            self._add_signed_distance_filtrations(binarizer_threshold)
            self._add_density_filtrations(binarizer_threshold)

    def _add_height_filtrations(self, binarizer_threshold: float):
        for direction in self.height_filtration_directions_:
            name = f'{int(binarizer_threshold * 10)}/HeightFiltrartion_{direction[0]}_{direction[1]}'
            extractor = FiltrationExtractor(
                gtda.images.HeightFiltration, { 'direction': numpy.array(direction) }, binarizer_threshold, **self.filtrations_kwargs_
            )
            self.filtration_extractors_.append((extractor, name))
            
    def _add_radial_filtrations(self, binarizer_threshold: float, radial_x: typing.List[int], radial_y: typing.List[int]):
        for center in list(itertools.product(radial_x, radial_y)):
            name = f'{int(binarizer_threshold * 10)}/RadialFiltration_{center[0]}_{center[1]}'
            extractor = FiltrationExtractor(
                gtda.images.RadialFiltration, { 'center': numpy.array(center) }, binarizer_threshold, **self.filtrations_kwargs_
            )
            self.filtration_extractors_.append((extractor, name))

    def _add_dilation_filtrations(self, binarizer_threshold: float):
        if self.reduced_:
            return
        name = f'{int(binarizer_threshold * 10)}/DilationFiltration'
        extractor = FiltrationExtractor(gtda.images.DilationFiltration, { }, binarizer_threshold, **self.filtrations_kwargs_)
        self.filtration_extractors_.append((extractor, name))

    def _add_erosion_filtrations(self, binarizer_threshold: float):
        if self.reduced_:
            return
        name = f'{int(binarizer_threshold * 10)}/ErosionFiltration'
        extractor = FiltrationExtractor(gtda.images.ErosionFiltration, { }, binarizer_threshold, **self.filtrations_kwargs_)
        self.filtration_extractors_.append((extractor, name))

    def _add_signed_distance_filtrations(self, binarizer_threshold: float):
        if self.reduced_:
            return
        name = f'{int(binarizer_threshold * 10)}/SignedDistanceFiltration'
        extractor = FiltrationExtractor(gtda.images.SignedDistanceFiltration, { }, binarizer_threshold, **self.filtrations_kwargs_)
        self.filtration_extractors_.append((extractor, name))
        
    def _add_density_filtrations(self, binarizer_threshold: float):
        if self.reduced_:
            return
        for radius in self.density_filtration_radiuses_:
            name = f'{int(binarizer_threshold * 10)}/DensityFiltration_{radius}'
            extractor = FiltrationExtractor(gtda.images.DensityFiltration, { 'radius': radius }, binarizer_threshold, **self.filtrations_kwargs_)
            self.filtration_extractors_.append((extractor, name))
