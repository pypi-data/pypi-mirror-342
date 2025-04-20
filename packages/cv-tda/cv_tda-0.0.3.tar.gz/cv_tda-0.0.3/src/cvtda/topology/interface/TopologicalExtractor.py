import abc
import typing

import numpy
import gtda.diagrams

from .. import utils
import cvtda.logging
import cvtda.dumping
from .Extractor import Extractor
from ..DiagramVectorizer import DiagramVectorizer

class TopologicalExtractor(Extractor):
    def __init__(
        self,
        supports_rgb: bool,
        n_jobs: int = -1,
        reduced: bool = True,
        only_get_from_dump: bool = False,
        topo_only_get_from_dump: bool = False,
        return_diagrams: bool = False,
        **kwargs
    ):
        super().__init__(
            n_jobs = n_jobs,
            reduced = reduced,
            only_get_from_dump = False,
            return_diagrams = return_diagrams,
            topo_only_get_from_dump = (topo_only_get_from_dump or only_get_from_dump),
            **kwargs
        )

        self.topo_only_get_from_dump_ = (topo_only_get_from_dump or only_get_from_dump)
        self.return_diagrams_ = return_diagrams
        self.supports_rgb_ = supports_rgb

        self.vectorizer_ = DiagramVectorizer(n_jobs = self.n_jobs_, reduced = self.reduced_)
        self.scaler_ = gtda.diagrams.Scaler(n_jobs = self.n_jobs_)
        

    def final_dump_name_(self, dump_name: typing.Optional[str] = None):
        return None
    
    def diagrams_dump_(self, dump_name: typing.Optional[str]):
        return cvtda.dumping.dump_name_concat(dump_name, "diagrams")
    
    def force_numpy_(self):
        return not self.return_diagrams_


    def process_rgb_(self, rgb_images: numpy.ndarray, do_fit: bool, dump_name: typing.Optional[str] = None):
        if not self.supports_rgb_:
            if self.return_diagrams_:
                return []
            else:
                return numpy.empty((len(rgb_images), 0))
        return self.do_work_(rgb_images, do_fit, dump_name)

    def process_gray_(self, gray_images: numpy.ndarray, do_fit: bool, dump_name: typing.Optional[str] = None):
        return self.do_work_(gray_images, do_fit, dump_name)
    
    def do_work_(self, images: numpy.ndarray, do_fit: bool, dump_name: typing.Optional[str] = None):
        if self.topo_only_get_from_dump_:
            if self.return_diagrams_:
                diagrams = cvtda.dumping.dumper().get_dump(self.diagrams_dump_(dump_name))
                cvtda.logging.logger().print("Applying Scaler to persistence diagrams.")
                return utils.process_iter(self.scaler_, diagrams, do_fit)
            else:
                return cvtda.dumping.dumper().get_dump(self.features_dump_(dump_name))

        diagrams = self.get_diagrams_(images, do_fit, dump_name)
        cvtda.logging.logger().print("Applying Scaler to persistence diagrams.")
        diagrams = utils.process_iter(self.scaler_, diagrams, do_fit)
        if self.return_diagrams_:
            return diagrams
        return utils.process_iter_dump(self.vectorizer_, diagrams, do_fit, self.features_dump_(dump_name))
    
    @abc.abstractmethod
    def get_diagrams_(self, images: numpy.ndarray, do_fit: bool, dump_name: typing.Optional[str] = None):
        pass