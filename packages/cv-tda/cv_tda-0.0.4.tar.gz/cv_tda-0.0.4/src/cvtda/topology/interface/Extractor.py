import abc
import typing

import numpy
import sklearn.base

import cvtda.utils
import cvtda.dumping
import cvtda.logging

from .. import utils
import cvtda.dumping

class Extractor(sklearn.base.TransformerMixin):
    def __init__(
        self,
        n_jobs: int = -1,
        reduced: bool = True,
        only_get_from_dump: bool = False,
        **kwargs
    ):
        self.n_jobs_ = n_jobs
        self.reduced_ = reduced
        self.only_get_from_dump_ = only_get_from_dump

        self.kwargs_ = kwargs
        self.kwargs_['n_jobs'] = n_jobs
        self.kwargs_['reduced'] = reduced
        self.kwargs_['only_get_from_dump'] = only_get_from_dump

        self.fitted_ = False
        self.fit_dimensions_ = None
    

    def final_dump_name_(self, dump_name: typing.Optional[str] = None):
        return self.features_dump_(dump_name)
    
    def features_dump_(self, dump_name: typing.Optional[str]):
        return cvtda.dumping.dump_name_concat(dump_name, "features")
    
    def force_numpy_(self):
        return True
    

    def fit(self, images: numpy.ndarray, dump_name: typing.Optional[str] = None):
        if self.only_get_from_dump_ and (len(images.shape) != 4):
            final_dump = self.final_dump_name_(dump_name)
            assert cvtda.dumping.dumper().has_dump(final_dump), f"There is no dump at {final_dump}"
        else:
            self.process_(images, do_fit = True, dump_name = dump_name)
        self.fitted_ = True
        return self
    
    def transform(self, images: numpy.ndarray, dump_name: typing.Optional[str] = None):
        assert self.fitted_ is True, 'fit() must be called before transform()'
        final_dump = self.final_dump_name_(dump_name)
        if (self.only_get_from_dump_ and (len(images.shape) != 4)) or cvtda.dumping.dumper().has_dump(final_dump):
            return cvtda.dumping.dumper().get_dump(final_dump)
        return self.process_(images, do_fit = False, dump_name = dump_name)
    
    def fit_transform(self, images: numpy.ndarray, dump_name: typing.Optional[str] = None):
        return self.fit(images, dump_name = dump_name).transform(images, dump_name = dump_name)


    def process_(self, images: numpy.ndarray, do_fit: bool, dump_name: typing.Optional[str] = None):
        if self.fit_dimensions_ is not None:
            assert self.fit_dimensions_ == images.shape[1:], \
                    f"The pipeline is fit for {self.fit_dimensions_}. Cannot use it with {images.shape}."
        
        if len(images.shape) == 4:
            assert images.shape[3] == 3, f'Images with {len(images.shape)} channels are not supported'
            cvtda.logging.logger().print("RGB images received. Transforming to grayscale.")

            rgb_dump = cvtda.dumping.dump_name_concat(dump_name, "rgb")
            gray_dump = cvtda.dumping.dump_name_concat(dump_name, "gray")
            red_dump = cvtda.dumping.dump_name_concat(dump_name, "red")
            green_dump = cvtda.dumping.dump_name_concat(dump_name, "green")
            blue_dump = cvtda.dumping.dump_name_concat(dump_name, "blue")
            saturation_dump = cvtda.dumping.dump_name_concat(dump_name, "saturation")
            value_dump = cvtda.dumping.dump_name_concat(dump_name, "value")

            if do_fit:
                self.gray_extractor_ = self.__class__(**self.kwargs_)
                self.red_extractor_ = self.__class__(**self.kwargs_)
                self.green_extractor_ = self.__class__(**self.kwargs_)
                self.blue_extractor_ = self.__class__(**self.kwargs_)
                if not self.reduced_:
                    self.saturation_extractor_ = self.__class__(**self.kwargs_)
                    self.value_extractor_ = self.__class__(**self.kwargs_)

            if self.only_get_from_dump_:
                rgb_data = cvtda.dumping.dumper().get_dump(self.final_dump_name_(rgb_dump))
            else:
                rgb_data = self.process_rgb_(images, do_fit, rgb_dump)

            gray_images = cvtda.utils.rgb2gray(images, self.n_jobs_)
            result = [
                rgb_data,
                utils.process_iter(self.gray_extractor_, gray_images, do_fit, gray_dump),
                utils.process_iter(self.red_extractor_, images[:, :, :, 0], do_fit, red_dump),
                utils.process_iter(self.green_extractor_, images[:, :, :, 1], do_fit, green_dump),
                utils.process_iter(self.blue_extractor_, images[:, :, :, 2], do_fit, blue_dump),
            ]
            if not self.reduced_:
                hsv = cvtda.utils.rgb2hsv(images, self.n_jobs_)
                result.append(utils.process_iter(self.saturation_extractor_, hsv[:, :, :, 1], do_fit, saturation_dump))
                result.append(utils.process_iter(self.value_extractor_, hsv[:, :, :, 2], do_fit, value_dump))
            
            result = utils.hstack(result, self.force_numpy_())
        else:
            assert len(images.shape) == 3, f'{len(images.shape) - 1}d images are not supported'
            result = self.process_gray_(images, do_fit, dump_name)
    
        self.fit_dimensions_ = images.shape[1:]
        return result
    
    @abc.abstractmethod
    def process_rgb_(self, rgb_images: numpy.ndarray, do_fit: bool, dump_name: typing.Optional[str] = None):
        pass
    
    @abc.abstractmethod
    def process_gray_(self, gray_images: numpy.ndarray, do_fit: bool, dump_name: typing.Optional[str] = None):
        pass
