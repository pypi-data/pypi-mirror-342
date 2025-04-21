import typing

import numpy
import gtda.images
import gtda.homology

import cvtda.utils
import cvtda.logging

from . import utils
from .interface import TopologicalExtractor


class GreyscaleExtractor(TopologicalExtractor):
    def __init__(
        self,
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
            **kwargs
        )

        self.persistence_ = gtda.homology.CubicalPersistence(homology_dimensions = [0, 1], n_jobs = self.n_jobs_)


    def get_diagrams_(self, images: numpy.ndarray, do_fit: bool, dump_name: typing.Optional[str] = None):
        cvtda.logging.logger().print(f"GreyscaleExtractor: processing {dump_name}, do_fit = {do_fit}")
        return utils.process_iter_dump(self.persistence_, images, do_fit, self.diagrams_dump_(dump_name))
