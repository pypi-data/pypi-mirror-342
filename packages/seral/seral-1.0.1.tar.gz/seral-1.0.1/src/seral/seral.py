import warnings
import numpy as np
from eral.eral_score import eral_score_with_normalization
from eral.time_series_helpers import _remove_nan_padding_single
from eral.time_series_alignment import sync_n_series_to_prototype, get_score_and_shift

class Cluster:
    """ Class representing a cluster in the evolving time series clustering

    The cluster is represented by two structures:
    - PSV (Prototype Shape Vector), which carries the shape of the prototype, representing the shapes of all samples used in
        updating the prototype
    - PCV (Prototype Confidence Vector), which describes how many input samples were used in conditioning the prototype at each
        time point

    The final prototype is obtained by combining PSV and PCV. The prototype is
    only defined in the time points where the PCV is greater than some user-defined threshold, for
    example 0.8 indicating that the prototype is defined at indices where at least 80% of the samples were used in
    conditioning the prototype.

    """

    psv: np.ndarray
    pcv: np.ndarray
    number_of_points: int
    alpha: float
    id: int
    eral_exclusion_zone: float = 0.2

    def __init__(self, sample: np.ndarray, id: int,  alpha: float = 0.1, exclusion_zone: float = 0.2):
        """ Initialize the cluster with a sample.

        Choosing :param:`alpha`: 1.0 --> only use region where all samples were used, results in a short prototype, 
        0.0 --> use all samples, results in a long prototype

        :param sample: Sample to be used as the prototype
        :param alpha: Threshold for the PCV: required proportion of samples to be used in conditioning the prototype.
        :param exclusion_zone: Exclusion zone for the alignment of the new sample to the prototype
        """

        self.psv = sample
        self.pcv = np.ones_like(sample)
        self.number_of_points = 1
        self.alpha = alpha
        self.id = id
        self.eral_exclusion_zone = exclusion_zone

    def try_add_sample(self, sample: np.ndarray, min_new_length: float = 0.8) -> bool:
        """ Try to add a new sample to the cluster

        The new sample is added to the cluster, if the new prototype would not be less than `min_new_length` times
        the length of the old prototype. If the new prototype would be too short, the sample is not added.

        If the sample is added, the prototype is updated, and the number of points is increased. True is returned.
        If the sample is not added, False is returned.

        :param sample: New sample to be added to the cluster
        :param min_new_length: Minimum length of the new prototype as a proportion of the old prototype
        :return: True if the sample was added, False if the sample was not added
        """

        if self.number_of_points == 0:
            raise ValueError("Cluster is not initialized, can not add samples")

        if min_new_length > 1:
            raise ValueError("min_new_length should be less than 1")
        
        new_psv, new_pcv, common_time = self._get_new_components(sample)

        start_idx, end_idx = self._calculate_crisp_prototype_boundaries(new_psv, new_pcv, self.alpha)
        new_prototype = new_psv[start_idx:end_idx]

        if len(new_prototype) / len(self.prototype) < min_new_length:
            return False

        self.psv = new_psv
        self.pcv = new_pcv
        self.number_of_points += 1
        # self.common_time = common_time

        return True

    def _get_alignment_of_sample_to_psv(self, sample: np.ndarray) -> int:
        """ Get the lag to be applied to the sample to align it to the PSV

        Using the crisp prototype, the lag is calculated. Then this lag is modified so that it can be applied to align the sample and the
        PSV.

        The sample must not be simply applied to the PSV, since the PSV contains
        ill-defined values at the edges.

        Attention: "Apply zero mean" is set to False in the call to :func:`eral.time_series_alignment.get_score_and_shift`.

        :param sample: Sample to be aligned to the prototype
        :return: Lag suitable to be applied to the sample to align it to the PSV
        """

        # Get current crisp prototype
        start_idx, end_idx = self._get_crisp_prototype_boundaries()
        prototype = self.psv[start_idx:end_idx]

        # Get optimal alignment of the new sample to the crisp prototype
        alignment: int = get_score_and_shift(prototype, sample, exclusion_zone=self.eral_exclusion_zone, apply_zero_mean=False)[1] # TODO: apply zero mean is fixed, check if it should be changed

        return alignment + start_idx

    def _get_shifted_sample_and_psv_with_alignment(self, sample: np.ndarray) -> tuple[np.ndarray, np.ndarray, int, np.ndarray]:
        """ Shift the sample and the PSV to align them

        Only the crisp prototype is used in the alignment. The PSV is then shifted to match the
        alignment of the sample and the crisp prototype.

        :param sample: Sample to be aligned to the prototype
        :return: Tuple of the shifted sample, the shifted PSV, alignment
        """

        alignment: int = self._get_alignment_of_sample_to_psv(sample)

        # Use obtained optimal alignment to shift the PSV
        psv = self.psv
        common_time, shifted_sample, shifted_psv = sync_n_series_to_prototype(prototype=psv,
                                                                              series=[sample],
                                                                              shifts=[alignment],
                                                                              exclusion_zone=self.eral_exclusion_zone)
        
        return shifted_sample[0], shifted_psv, alignment, common_time

    def _get_shifted_sample_and_psv(self, sample: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """ Shift the sample and the PSV to align them 
        
        Only the crisp prototype is used in the alignment. The PSV is then shifted to match the
        alignment of the sample and the crisp prototype.

        :param sample: Sample to be aligned to the prototype
        :return: Tuple of the shifted sample and the shifted PSV
        """

        shifted_sample, shifted_psv, _, _ = self._get_shifted_sample_and_psv_with_alignment(sample)
        
        return shifted_sample, shifted_psv


    def _generate_new_pcv(self, start_idx: int, end_idx: int) -> np.ndarray:
        """ Generate a new PCV when adding new sample to the cluster 
        
        The region where the new sample is added to the cluster has increased support after the addition. The
        PCV is updated to reflect this change.

        :param start_idx: Start index of the new sample in the PSV
        :param end_idx: End index of the new sample in the PSV
        :return: New PCV
        """

        previous_number_of_points = self.number_of_points
        new_number_of_points = previous_number_of_points + 1

        old_pcv = self.pcv
        new_pcv = old_pcv.copy() * previous_number_of_points
        if start_idx < 0:
            new_pcv = np.concatenate([np.zeros(-start_idx), new_pcv])
            end_idx+=-start_idx
            start_idx = 0
        if end_idx > len(new_pcv):
            new_pcv = np.concatenate([new_pcv, np.zeros(end_idx - len(new_pcv))])
            end_idx = len(new_pcv)

        new_pcv[start_idx:end_idx] += 1

        new_pcv /= new_number_of_points

        return new_pcv

    def _generate_new_psv(self, aligned_sample: np.ndarray, aligned_psv: np.ndarray) -> np.ndarray:
        """ Generate a new PSV by adding the new aligned sample to the existing PSV """

        assert len(aligned_sample) == len(aligned_psv), ("Aligned sample and aligned PSV should have the same length. "
                                                                        f"Lengths are {len(aligned_sample)} and "
                                                                        f"{len(aligned_psv)}")
        
        # Calculate the weights
        weight_new_sample = 1 / (self.number_of_points + 1)
        weight_old_prototype = self.number_of_points / (self.number_of_points + 1)

        # Calculate the new prototype
        
        aligned_psv_nan_mask = np.isnan(aligned_psv)
        aligned_sample_nan_mask = np.isnan(aligned_sample)

        sample_weights_vector = np.zeros_like(aligned_sample)+weight_new_sample
        prototype_weights_vector = np.zeros_like(aligned_psv)+weight_old_prototype
        # Weights should be weight_new_sample and weight_old_prototype where neither of the values is NaN
        pass

        # At regions where only the sample is NaN, the prototype should be used
        sample_weights_vector[aligned_sample_nan_mask] = 0
        prototype_weights_vector[aligned_sample_nan_mask] = 1

        # At regions where only the prototype is NaN, the sample should be used
        sample_weights_vector[aligned_psv_nan_mask] = 1
        prototype_weights_vector[aligned_psv_nan_mask] = 0

        # The sum of the weights should be 1
        assert np.allclose(sample_weights_vector+prototype_weights_vector, 1), ("Sample and prototype weights should sum to 1")

        weighted_new_sample = aligned_sample * sample_weights_vector
        weighted_old_prototype = aligned_psv * prototype_weights_vector

        new_prototype = np.nansum(np.array([weighted_old_prototype, weighted_new_sample]), axis=0)
        
        return new_prototype

    def _get_new_components(self, sample: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """ Get the new PSV, the new PCV, and the common time points
        
        The new sample is aligned to the existing crisp prototype. The lag is used to align the sample and the
        PSV. The PSV is then updated by adding the new sample to the prototype.

        The PCV is updated to reflect the latest update.

        This method does not update the cluster, only calculates the new components.

        :param sample: New sample to be added to the cluster
        :return: Tuple of the new PSV, the new PCV, and the common time points
        """

        shifted_sample, shifted_psv, alignment, common_time = self._get_shifted_sample_and_psv_with_alignment(sample)
        assert len(shifted_sample) == len(shifted_psv), ("Shifted sample and shifted PSV should have the same length. "
                                                                        f"Lengths are {len(shifted_sample)} and "
                                                                        f"{len(shifted_psv)}")

        new_pcv = self._generate_new_pcv(start_idx=alignment, end_idx=alignment+len(sample))

        new_psv = self._generate_new_psv(shifted_sample, shifted_psv)

        assert len(new_psv) == len(new_pcv), ("New PSV and new PCV should have the same length. "
                                                                            f"Lengths are {len(new_psv)} and "
                                                                            f"{len(new_pcv)}")
        
        return new_psv, new_pcv, common_time

    def add_sample(self, sample: np.ndarray):
        """ Add a new sample to the cluster

        The new sample is aligned to the existing crisp prototype. The lag is used to align the sample and the
        PSV. The PSV is then updated by adding the new sample to the prototype.

        The PCV is updated to reflect the latest update.

        :param sample: New sample to be added to the cluster
        :return: None
        """

        new_psv, new_pcv, common_time = self._get_new_components(sample)

        # self.common_time = common_time
        self.psv = new_psv
        self.pcv = new_pcv
        self.number_of_points += 1

    @staticmethod
    def distance(prototype: np.ndarray, sample: np.ndarray, eral_exclusion_zone: float) -> float:
        """ Calculate the distance between the prototype and the sample

        ERAL score with normalization is used to calculate the error in alignment of the sample to the prototype.
        Normalization in ERAL score is done by the length of the overlap of the sample and the prototype.

        ERAL score is further multiplied by (len_sample*len_prototype)/(overlap_len^2) to penalize short overlaps.

        :param prototype: Prototype to be compared to the sample
        :param sample: Sample to be compared to the prototype
        :param eral_exclusion_zone: Exclusion zone for the alignment of the new sample to the prototype
        :return: Distance
        """

        a = _remove_nan_padding_single(prototype)
        b = _remove_nan_padding_single(sample)
        eral_score, normalization = eral_score_with_normalization(a, b)

        if eral_exclusion_zone > 0:
            # Exclude the forbidden shifts
            exclusion_zone = int(len(eral_score) * eral_exclusion_zone)
            eral_score[:exclusion_zone] = np.inf
            eral_score[-exclusion_zone:] = np.inf

        eral_dist = np.min(eral_score)
        normalization = normalization[np.argmin(eral_score)]

        overlap_len = normalization ** 2

        prototype_len = len(_remove_nan_padding_single(prototype))
        sample_len = len(_remove_nan_padding_single(sample))
        factor = (prototype_len * sample_len) / (overlap_len ** 2)

        return eral_dist * normalization * (factor ** 2)

    def calculate_distance(self, sample: np.ndarray) -> float:
        """ Calculate the distance of the sample to the prototype, using the ERAL score

        ERAL score with normalization is used to calculate the error in alignment of the sample to the prototype.
        Normalization in ERAL score is done by the length of the overlap of the sample and the prototype.

        ERAL score is further multiplied by (len_sample*len_prototype)/(overlap_len^2) to penalize short overlaps.

        :param sample: Sample to be compared to the prototype
        :return: Distance
        """

        return self.distance(self.prototype, sample, self.eral_exclusion_zone)


    @staticmethod
    def _calculate_crisp_prototype_boundaries(psv: np.ndarray, pcv: np.ndarray, alpha: float) -> tuple[int, int]:
        """ Get the start and end index of the crisp prototype in the PSV

        The crisp prototype is defined in the time points where the PCV is greater than some user-defined
        threshold, for example 0.8 indicating that the prototype is defined at indices where at least 80% of the
        samples were used in conditioning the prototype.

        Choosing :param:`alpha`: 1.0 --> only use region where all samples were used, results in a short prototype, 
        0.0 --> use all samples, results in a long prototype

        :param psv: Prototype Shape Vector
        :param pcv: Prototype Confidence Vector
        :param alpha: Threshold for the PCV: required proportion of samples to be used in conditioning the prototype.
        :return: Tuple of the start and end index of the crisp prototype in the PSV
        """

        assert len(psv) == len(pcv), ("PSV and PCV should have the same length")

        bounding_filter = pcv >= alpha
        start_idx = np.argmax(bounding_filter)
        end_idx = len(bounding_filter) - np.argmax(bounding_filter[::-1])
        return start_idx, end_idx


    def _get_crisp_prototype_boundaries(self) -> tuple[int, int]:
        """ Get the start and end index of the crisp prototype in the PSV

        The crisp prototype is defined in the time points where the PCV is greater than some user-defined
        threshold, for example 0.8 indicating that the prototype is defined at indices where at least 80% of the
        samples were used in conditioning the prototype.

        :return: Tuple of the start and end index of the crisp prototype in the PSV
        """

        start_idx, end_idx = self._calculate_crisp_prototype_boundaries(self.psv, self.pcv, self.alpha)

        return start_idx, end_idx


    def _prototype_defuzzification(self) -> np.ndarray:
        """ Returns the prototype of the cluster

        The prototype is obtained by combining the PSV and the PCV. The prototype is
        only defined in the time points where the PCV is greater than some user-defined threshold, for
        example 0.8 indicating that the prototype is defined at indices where at least 80% of the samples were used
        in conditioning the prototype.

        :return: Crisp prototype
        """

        start_idx, end_idx = self._get_crisp_prototype_boundaries()

        return self.psv[start_idx:end_idx]

    @property
    def prototype(self) -> np.ndarray:
        """ Get the prototype of the cluster """
        return self._prototype_defuzzification()


    def copy(self, deep: bool = False, new_id: int | None = None) -> 'Cluster':
        """ Create a copy of the cluster

        :param deep: If True, a deep copy is made. If False, a shallow copy is made.
        :return: Copy of the cluster
        """

        if new_id is None:
            new_id = self.id

        if not deep:
            new_cluster = self.__class__(sample=self.psv)
            new_cluster.pcv = self.pcv.copy()
            new_cluster.number_of_points = self.number_of_points
            new_cluster.alpha = self.alpha
            new_cluster.id = new_id
            new_cluster.eral_exclusion_zone = self.eral_exclusion_zone
            return new_cluster
        
        new_cluster = self.__class__(sample=self.psv.copy(), id = new_id)
        new_cluster.pcv = self.pcv.copy()
        new_cluster.number_of_points = self.number_of_points
        new_cluster.alpha = self.alpha
        new_cluster.eral_exclusion_zone = self.eral_exclusion_zone
        return new_cluster
    
    def merge(self, other_cluster: 'Cluster', new_alpha: float | None = None, new_id: int | None = None):
        """ Force merge the other cluster into this cluster
        
        The other cluster is added to this cluster. The prototype is updated by adding the prototype of the other
        cluster to the prototype of this cluster. The PCV is updated to reflect the new number of points.
        
        :param other_cluster: Cluster to be merged into this cluster
        :param new_alpha: New alpha value for the merged cluster. If None, the alpha value of this cluster is used.
        :param new_id: New id for the merged cluster. If None, the id of this cluster is used.
        """

        success = self.try_merge(other_cluster, new_alpha, new_id, new_min_length=0)
        if not success:
            raise Exception("Merge was not successful")
        return

    def try_merge(self, other_cluster: 'Cluster', new_alpha: float | None = None, new_id: int | None = None, min_new_length: float = 0.9) -> bool:
        """ Try to merge the other cluster into this cluster

        The other cluster is added to this cluster. The prototype is updated by adding the prototype of the other
        cluster to the prototype of this cluster. The PCV is updated to reflect the new number of points.

        If the new prototype would be less than `min_new_length` times the length of the old prototype, the merge is not
        performed, False is returned.

        :param other_cluster: Cluster to be merged into this cluster
        :param new_alpha: New alpha value for the merged cluster. If None, the alpha value of this cluster is used.
        :param new_id: New id for the merged cluster. If None, the id of this cluster is used.
        :param min_new_length: Minimum length of the new prototype as a proportion of the old prototype.
        :return: True if the merge was successful, False if the merge was not successful (new prototype would be too short)
        """

        if not isinstance(other_cluster, Cluster):
            raise ValueError(f"Can only merge with another Cluster object, not {type(other_cluster)}")

        my_psv = self.psv
        my_pcv = self.pcv
        my_count = self.number_of_points
        other_psv = other_cluster.psv
        other_pcv = other_cluster.pcv
        other_count = other_cluster.number_of_points

        if new_alpha is None:
            new_alpha = self.alpha
        if new_id is None:
            new_id = self.id

        # my_prototype = self.prototype
        # other_prototype = other_cluster.prototype
        my_prototype_start, my_prototype_end = self._get_crisp_prototype_boundaries()
        my_prototype = my_psv[my_prototype_start:my_prototype_end]
        other_prototype_start, other_prototype_end = other_cluster._get_crisp_prototype_boundaries()
        other_prototype = other_psv[other_prototype_start:other_prototype_end]
        
        # Align the prototypes
        prototype_alignment = get_score_and_shift(my_prototype, other_prototype, exclusion_zone=self.eral_exclusion_zone, apply_zero_mean=False)[1] # TODO: apply zero mean is fixed, check if it should be changed
        alignment = prototype_alignment + my_prototype_start - other_prototype_start
        

        # Calculate the new PCV
        # alignment: int = self._get_alignment_of_sample_to_psv(other_prototype)

        _, shifted_other_pcv, shifted_my_pcv = sync_n_series_to_prototype(prototype=my_pcv,
                                                                                    series=[other_pcv],
                                                                                    shifts=[alignment])
        shifted_other_pcv = shifted_other_pcv[0]
        shifted_other_pcv = np.nan_to_num(shifted_other_pcv, nan=0)
        shifted_my_pcv = np.nan_to_num(shifted_my_pcv, nan=0)
        new_pcv = (my_count * shifted_my_pcv + other_count * shifted_other_pcv) / (my_count + other_count)
        
        # Calculate the new PSV
        _, shifted_other_psv, shifted_my_psv = sync_n_series_to_prototype(prototype=my_psv,
                                                                                    series=[other_psv],
                                                                                    shifts=[alignment])
        shifted_other_psv = shifted_other_psv[0]

        weight_my_psv = my_count / (my_count + other_count)
        weight_other_psv = other_count / (my_count + other_count)

        aligned_my_psv_nan_mask = np.isnan(shifted_my_psv)
        aligned_other_psv_nan_mask = np.isnan(shifted_other_psv)
        
        my_psv_weights_vector = np.zeros_like(shifted_my_psv)+weight_my_psv
        other_psv_weights_vector = np.zeros_like(shifted_other_psv)+weight_other_psv        
        # Weights should be weight_my_psv and weight_other_psv where neither of the values is NaN
        pass

        # At regions where only my_psv is NaN, other_psv should be used
        my_psv_weights_vector[aligned_my_psv_nan_mask] = 0
        other_psv_weights_vector[aligned_my_psv_nan_mask] = 1

        # At regions where only other_psv is NaN, my_psv should be used
        my_psv_weights_vector[aligned_other_psv_nan_mask] = 1
        other_psv_weights_vector[aligned_other_psv_nan_mask] = 0

        # The sum of the weights should be 1
        assert np.allclose(my_psv_weights_vector+other_psv_weights_vector, 1), ("My PSV and other PSV weights should sum to 1")

        weighted_my_psv = shifted_my_psv * my_psv_weights_vector
        weighted_other_psv = shifted_other_psv * other_psv_weights_vector

        new_psv = np.nansum(np.array([weighted_my_psv, weighted_other_psv]), axis=0)

        # Remove padding where pcv is 0
        start_idx = np.argmax(new_pcv>0)
        end_idx = len(new_pcv) - np.argmax(new_pcv[::-1]>0)
        new_psv = new_psv[start_idx:end_idx]
        new_pcv = new_pcv[start_idx:end_idx]
        
        assert len(new_psv) == len(new_pcv), ("New PSV and new PCV should have the same length.")

        final_prototype_start_idx, final_prototype_end_idx = self._calculate_crisp_prototype_boundaries(new_psv, new_pcv, new_alpha)
        final_prototype_length = final_prototype_end_idx - final_prototype_start_idx

        if final_prototype_length < len(my_prototype)*min_new_length:
            return False

        # Update the cluster
        self.psv = new_psv
        self.pcv = new_pcv
        self.number_of_points += other_count
        self.alpha = new_alpha
        self.id = new_id

        return True
