import typing

import numpy
import joblib
import sklearn.base
import gtda.diagrams

import cvtda.utils
import cvtda.logging


class DiagramVectorizer(sklearn.base.TransformerMixin):
    def __init__(
        self,
        n_jobs: int = -1,
        reduced: bool = True,

        n_bins: int = 64,
        batch_size: int = 512,
        filtering_percentile: int = 10,
        
        persistence_landscape_layers: int = 3,
        silhouette_powers: typing.List[int] = [ 1, 2 ],
        heat_kernel_sigmas: typing.List[float] = [ 0.1, 1.0, numpy.pi ],
        persistence_image_sigmas: typing.List[float] = [ 0.1, 1.0, numpy.pi ]
    ):
        self.fitted_ = False
        self.n_jobs_ = n_jobs
        self.reduced_ = reduced
        self.batch_size_ = batch_size
        self.filtering_percentile_ = filtering_percentile
        
        self.betti_curve_ = gtda.diagrams.BettiCurve(n_bins = n_bins, n_jobs = 1)

        self.persistence_landscape_ = gtda.diagrams.PersistenceLandscape(
            n_layers = persistence_landscape_layers,
            n_bins = n_bins,
            n_jobs = 1
        )

        self.silhouettes_ = [
            gtda.diagrams.Silhouette(power = power, n_bins = n_bins, n_jobs = 1)
            for power in silhouette_powers
        ]
        
        self.persistence_entropy_ = gtda.diagrams.PersistenceEntropy(nan_fill_value = 0, n_jobs = 1)
        
        self.number_of_points_ = gtda.diagrams.NumberOfPoints(n_jobs = 1)
        
        self.heat_kernels_ = [
            gtda.diagrams.HeatKernel(sigma = sigma, n_bins = n_bins, n_jobs = 1)
            for sigma in heat_kernel_sigmas
        ]
        
        self.persistence_images_ = [
            gtda.diagrams.PersistenceImage(sigma = sigma, n_bins = n_bins, n_jobs = 1)
            for sigma in persistence_image_sigmas
        ]


    def fit(self, diagrams: numpy.ndarray):
        self.homology_dimensions_ = numpy.unique(diagrams[:, :, 2])
        
        self.filtering_epsilon_ = self.determine_filtering_epsilon_(diagrams)
        self.filtering_ = gtda.diagrams.Filtering(epsilon = self.filtering_epsilon_).fit(diagrams)

        self.betti_curve_.fit(diagrams)
        
        self.persistence_landscape_.fit(diagrams)
        
        for silhouette in self.silhouettes_:
            silhouette.fit(diagrams)
        
        self.persistence_entropy_.fit(diagrams)
        
        self.number_of_points_.fit(diagrams)

        for heat_kernel in self.heat_kernels_:
            heat_kernel.fit(diagrams)
            
        for persistence_image in self.persistence_images_:
            persistence_image.fit(diagrams)

        cvtda.logging.logger().print('DiagramVectorizer: fitting complete')
        self.fitted_ = True
        return self
    
    def transform(self, diagrams: numpy.ndarray) -> numpy.ndarray:
        assert self.fitted_ is True, 'fit() must be called before transform()'
        
        def transform_batch(batch: numpy.ndarray) -> numpy.ndarray:
            batch = self.filtering_.transform(batch)
            return numpy.hstack([
                self.calc_betti_features_            (batch),
                self.calc_landscape_features_        (batch),
                self.calc_silhouette_features_       (batch),
                self.calc_entropy_features_          (batch),
                self.calc_number_of_points_features_ (batch),
                self.calc_heat_features_             (batch),
                self.calc_persistence_image_features_(batch),
                self.calc_lifetime_features_         (batch)
            ])
        
        loop = range(0, len(diagrams), self.batch_size_)
        features = joblib.Parallel(return_as = 'generator', n_jobs = self.n_jobs_)(
            joblib.delayed(transform_batch)(diagrams[batch_start:batch_start + self.batch_size_])
            for batch_start in loop
        )

        collector = cvtda.logging.logger().pbar(features, total = len(loop), desc = 'DiagramVectorizer: batch')
        return numpy.vstack(list(collector))



    def determine_filtering_epsilon_(self, diagrams: numpy.ndarray) -> float:
        life = (diagrams[:, :, 1] - diagrams[:, :, 0]).flatten()
        return numpy.percentile(life[life != 0], self.filtering_percentile_)

    def calc_perdim_sequence_stats_(self, data: numpy.ndarray) -> numpy.ndarray:
        return numpy.hstack([
            cvtda.utils.sequence2features(data[:, dim, :], reduced = self.reduced_)
            for dim in range(data.shape[1])
        ])
    


    def calc_betti_features_(self, diagrams: numpy.ndarray) -> numpy.ndarray:
        betti_curves = self.betti_curve_.transform(diagrams)
        return self.calc_perdim_sequence_stats_(betti_curves)
        
    def calc_landscape_features_(self, diagrams: numpy.ndarray) -> numpy.ndarray:
        n_layers = self.persistence_landscape_.n_layers
        landscape = self.persistence_landscape_.transform(diagrams)
        return numpy.hstack([
            self.calc_perdim_sequence_stats_(landscape[:, layer::n_layers, :])
            for layer in range(n_layers)
        ])

    def calc_silhouette_features_(self, diagrams: numpy.ndarray) -> numpy.ndarray:
        return numpy.hstack([
            self.calc_perdim_sequence_stats_(silhouette.transform(diagrams))
            for silhouette in self.silhouettes_
        ])

    def calc_entropy_features_(self, diagrams: numpy.ndarray) -> numpy.ndarray:
        return self.persistence_entropy_.transform(diagrams)
    
    def calc_number_of_points_features_(self, diagrams: numpy.ndarray) -> numpy.ndarray:
        return self.number_of_points_.transform(diagrams)
    
    def calc_heat_features_(self, diagrams: numpy.ndarray) -> numpy.ndarray:
        flat_shape = (len(diagrams), len(self.homology_dimensions_), -1)
        return numpy.hstack([
            self.calc_perdim_sequence_stats_(heat_kernel.transform(diagrams).reshape(flat_shape))
            for heat_kernel in self.heat_kernels_
        ])
        
    def calc_persistence_image_features_(self, diagrams: numpy.ndarray) -> numpy.ndarray:
        flat_shape = (len(diagrams), len(self.homology_dimensions_), -1)
        return numpy.hstack([
            self.calc_perdim_sequence_stats_(persistence_image.transform(diagrams).reshape(flat_shape))
            for persistence_image in self.persistence_images_
        ])

    def calc_lifetime_features_(self, diagrams: numpy.ndarray) -> numpy.ndarray:
        birth, death, dim = diagrams[:, :, 0], diagrams[:, :, 1], diagrams[:, :, 2]
        bd2 = (birth + death) / 2.0
        life = death - birth

        bd2_bulk = [ ]
        life_bulk = [ ]
        for d in self.homology_dimensions_:
            mask = (dim != d) | (life < self.filtering_epsilon_)
            bd2_bulk.append(numpy.ma.array(bd2, mask = mask))
            life_bulk.append(numpy.ma.array(life, mask = mask))

        return numpy.hstack([
            self.calc_perdim_sequence_stats_(numpy.ma.stack(bd2_bulk, axis = 1)),
            self.calc_perdim_sequence_stats_(numpy.ma.stack(life_bulk, axis = 1))
        ])
