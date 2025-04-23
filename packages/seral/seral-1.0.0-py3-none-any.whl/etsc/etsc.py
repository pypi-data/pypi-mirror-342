import warnings
import numpy as np
# from eral.time_series_helpers import _remove_nan_padding_single, _var_nan_sum
# from eral.time_series_alignment import sync_n_series_to_prototype, get_score_and_shift
# from .batch_cluster import BatchCluster as Cluster
from src.seral.seral import Cluster

from collections.abc import Generator

class EvolvingTimeSeriesClustering:  

    clusters: list[Cluster]
    outlier_clusters: list[Cluster]
    threshold: float
    exclusion_zone: float
    new_min_length: float
    alpha: float
    outlier_percentage: float
    verbose: bool

    def __init__(self, threshold: float|None = None, exclusion_zone: float = 0.2, new_min_length: float = 0.8, alpha: float = 0.1, outlier_percentage: float = 0.01, verbose: bool = True):
        """ Initialize the evolving time series clustering

        Choosing :param:`alpha`: 1.0 --> only use region where all samples were used, results in a short prototype, 
        0.0 --> use all samples, results in a long prototype

        :param threshold: Maximum distance to the closest cluster for the sample to be added to the cluster
        :param exclusion_zone: Exclusion zone for the alignment of the new sample to the prototype
        :param new_min_length: Minimum length of the new prototype as a proportion of the old prototype
        :param alpha: Threshold for PCV: required proportion of samples to be used in conditioning the prototype.
        """

        self.clusters = []
        self.outlier_clusters = []
        self.exclusion_zone = exclusion_zone
        self.threshold = threshold
        self.min_new_length = new_min_length
        self.alpha = alpha
        self.max_outlier_points = 0
        self.cluster_generator = self.get_cluster_id()
        self.outlier_percentage = outlier_percentage
        self.verbose = verbose
        self.next_cluster_id = 0

        super().__init__()

    def _get_threshold_curve(self, data: list[np.ndarray], expected_number_of_clusters: int):
        D = []
        for i, x in enumerate(data):
            d = []
            for j, y in enumerate(data):
                if i == j:
                    continue
                distance = Cluster.distance(x, y, self.exclusion_zone)
                d.append(distance)
            # D.append(np.min(d))
            D.append(np.percentile(d,100/(2*expected_number_of_clusters)))
        return D

    def estimate_threshold(self, data: list[np.ndarray], expected_number_of_clusters: int, percentile: float = 0.95) -> float:
        """ Estimate the threshold for the clustering

        The threshold is estimated as the `percentile`-th percentile of the distances of the samples to their closest neighbors.

        Configures the self.threshold attribute.
        
        :param data: List of samples to be used for the estimation
        :param percentile: Percentile of the distances to be used as the threshold
        :return: Estimated threshold

        """
        if percentile < 0 or percentile > 100:
            raise ValueError("Percentile must be between 0 and 100")

        D = self._get_threshold_curve(data, expected_number_of_clusters)
        
        if 0 <= percentile <= 1:
            percentile = percentile*100
        
        self.threshold = np.percentile(D, percentile)
        return self.threshold

    def fit_predict(self, data: list[np.ndarray]) -> list[int]:
        """ Fit the data to the clusters and return the cluster indices"""
        y_pred = []
        for i, sample in enumerate(data):
            y = self.fit_point(sample-np.mean(sample))
            y_pred.append(y)

            merge_success, merge_ids = self.try_merge_clusters(merge_threshold=self.threshold, id=y)
            if merge_success:
                new_id, old_id = merge_ids
                if self.verbose:
                    print(f"Merged {old_id} into {new_id}")
                y_pred = [new_id if x==old_id else x for x in y_pred]

        return y_pred

    def get_cluster_id(self) ->  Generator[list[int], None, None]:
        """ Generator for cluster ids

        :return: Generator for cluster ids
        """
        while True:
            cluster_id = self.next_cluster_id
            self.next_cluster_id += 1
            yield cluster_id

    def try_promote_outlier(self, id: int | None = None) -> bool:
        """ Try to promote outlier clusters to regular clusters.

        Only promotes a single cluster at a time.
        
        If no id is provided, the outlier cluster with the most points is tested for promotion. If an id is provided, the outlier
        cluster with that id is tested for promotion.

        :param id: Id of the outlier cluster to be tested for promotion
        :return: True if a cluster was promoted, False otherwise
        """
        if id is None:
            sorted_clusters = sorted(self.outlier_clusters, key=lambda x: x.number_of_points, reverse=True)
            cluster_under_test = sorted_clusters[0]
        else:
            cluster_under_test = [cluster for cluster in self.outlier_clusters if cluster.id == id][0]
        
        if cluster_under_test.number_of_points > self.max_outlier_points:
            self.clusters.append(cluster_under_test)
            self.outlier_clusters.remove(cluster_under_test)
            if self.verbose:
                print(f"Outlier cluster {cluster_under_test.id} was promoted to a regular cluster. Now {len(self.clusters)} regular clusters and {len(self.outlier_clusters)} outlier clusters.")
            return True
        return False


    def try_demote_cluster(self) -> bool:
        """ Try to demote regular clusters to outlier clusters.
        
        If a cluster has fewer points than the threshold, it is demoted to an outlier cluster.

        Only demotes a single cluster at a time.

        :return: True if a cluster was demoted, False otherwise
        """

        for cluster in self.clusters:
            if cluster.number_of_points < self.max_outlier_points:
                self.outlier_clusters.append(cluster)
                self.clusters.remove(cluster)
                if self.verbose:
                    print(f"Cluster {cluster.id} was demoted to an outlier cluster. Now {len(self.clusters)} regular clusters and {len(self.outlier_clusters)} outlier clusters.")
                return True
        return False
    
    def try_merge_clusters(self, id: int | None, merge_threshold: float) -> tuple[bool, tuple[int, int] | None]:
        """ Try to merge clusters
        
        If two clusters are closer than the threshold, they are merged into a single cluster.
        
        Only merges a single pair of clusters at a time.
        
        :param id: Id of the cluster to be tested for merging
        :param merge_threshold: Threshold for merging clusters
        :return: Tuple of a boolean indicating whether a merge was performed and the ids of the merged clusters
        """

        # Check outlier clusters
        for i, cluster1 in enumerate(self.outlier_clusters):
            for j, cluster2 in enumerate(self.outlier_clusters):
                if id is not None:
                    if cluster1.id != id and cluster2.id != id:
                        continue
                if i != j and cluster1.calculate_distance(cluster2.prototype) < merge_threshold:
                    merge_result = cluster1.try_merge(cluster2)
                    if merge_result is False:
                        continue
                    self.outlier_clusters.remove(cluster2)
                    if self.verbose:
                        print(f"Outlier clusters {cluster1.id} and {cluster2.id} were merged. Now {len(self.clusters)} regular clusters and {len(self.outlier_clusters)} outlier clusters.")
                    return True, (cluster1.id, cluster2.id)
        
    
        # Check merging outliers to regular clusters
        for i, cluster1 in enumerate(self.clusters):
            for j, cluster2 in enumerate(self.outlier_clusters):
                if id is not None:
                    if cluster1.id != id and cluster2.id != id:
                        continue
                if cluster1.calculate_distance(cluster2.prototype) < merge_threshold:
                    merge_result = cluster1.try_merge(cluster2)
                    if merge_result is False:
                        continue
                    self.outlier_clusters.remove(cluster2)
                    if self.verbose:
                        print(f"Outlier cluster {cluster2.id} was merged into regular cluster {cluster1.id}. Now {len(self.clusters)} regular clusters and {len(self.outlier_clusters)} outlier clusters.")
                    return True, (cluster1.id, cluster2.id)
                
        # Check regular clusters
        for i, cluster1 in enumerate(self.clusters):
            for j, cluster2 in enumerate(self.clusters):
                if id is not None:
                    if cluster1.id != id and cluster2.id != id:
                        continue
                if i != j and cluster1.calculate_distance(cluster2.prototype) < merge_threshold:
                    merge_result = cluster1.try_merge(cluster2)
                    if merge_result is False:
                        continue
                    self.clusters.remove(cluster2)
                    if self.verbose:
                        print(f"Clusters {cluster1.id} and {cluster2.id} were merged. Now {len(self.clusters)} regular clusters and {len(self.outlier_clusters)} outlier clusters.")
                    return True, (cluster1.id, cluster2.id)
                
        return False, None


    def fit_point(self, data, verbose: bool = True) -> int:
        """ Fit a new data point to the clusters

        The data point is fitted to the existing clusters. If the distance to the closest cluster is less than `threshold`,
        the data point is added to the cluster. If the distance is greater than `threshold`, a new cluster is created.

        When adding the data point to the cluster, if the new prototype would be less than `min_new_length` times the
        length of the old prototype, the data point is not added to the cluster. Instead, the next closest cluster is
        evaluated, up to the point where the distance is greater than `threshold`. If no cluster is found, a new cluster is
        generated

        :param data: Data point to be fitted to the clusters
        :return cluster index: Index of the cluster to which the data point was added
        """

        if self.threshold is None:
            raise ValueError("Threshold must be set before fitting data points. Use the estimate_threshold method to estimate the threshold.")

        self.max_outlier_points = (np.sum([cluster.number_of_points for cluster in self.clusters]) + np.sum([cluster.number_of_points for cluster in self.outlier_clusters]))*self.outlier_percentage
        if len(self.clusters) == 0:
            self.clusters.append(Cluster(sample=data, alpha=self.alpha, id=next(self.cluster_generator)))
            return self.clusters[-1].id
        else:
            # Try to add to existing clusters
            distances = self.calculate_distances(data)
            while np.min(distances) < self.threshold:
                closest_cluster = np.argmin(distances)
                if distances[closest_cluster] < self.threshold:
                    add_sample_result: bool = self.clusters[closest_cluster].try_add_sample(data,
                                                                                            self.min_new_length)
                    if add_sample_result is True:
                        return self.clusters[closest_cluster].id
                    warnings.warn("Sample was not added to the cluster, trying next closest cluster",
                                  category=UserWarning)
                    distances[closest_cluster] = np.inf
            #Try to add to outlier clusters
            if len(self.outlier_clusters) > 0:
                self.try_demote_cluster()
                distances = np.array([cluster.calculate_distance(data) for cluster in self.outlier_clusters])
                while np.min(distances) < self.threshold:
                    # Try to add to existing outlier clusters
                    closest_cluster = np.argmin(distances)
                    if distances[closest_cluster] < self.threshold:
                        add_sample_result: bool = self.outlier_clusters[closest_cluster].try_add_sample(data,
                                                                                                self.min_new_length)
                        if add_sample_result is True:
                            # Perhaps the outlier cluster has enough points to be promoted
                            if self.try_promote_outlier(self.outlier_clusters[closest_cluster].id):
                                # The outlier cluster was promoted and appended to the regular clusters
                                return self.clusters[-1].id
                            
                            return self.outlier_clusters[closest_cluster].id
                        # Unsuccessful add, try next closest outlier cluster
                        warnings.warn("Sample was not added to the outlier cluster, trying next closest outlier cluster",
                                    category=UserWarning)
                        distances[closest_cluster] = np.inf
                else:
                    self.outlier_clusters.append(Cluster(sample=data, alpha=self.alpha, id=next(self.cluster_generator)))
                    return self.outlier_clusters[-1].id
            else:                # Create first outlier cluster
                self.outlier_clusters.append(Cluster(sample=data, alpha=self.alpha, id=next(self.cluster_generator)))
                return self.outlier_clusters[-1].id
            
    def predict(self, sample: np.ndarray, prefer_established: bool = True, only_established: bool = True, threshold=None) -> int:
        """ Predict the cluster of the sample

        :param sample: Sample to be predicted
        :param prefer_established: If True, prefer established clusters over outlier clusters
        :param only_established: If True, only established clusters are considered for prediction
        :param threshold: Threshold for the prediction. If None, the threshold of the clustering model is used.
        :return: Cluster id of the predicted cluster or -1 if no cluster was found within the threshold
        """
        if threshold is None:
            threshold = self.threshold

        distances_established = self.calculate_distances(sample)
        if not only_established:
            distances_outlier = [cluster.calculate_distance(sample) for cluster in self.outlier_clusters]

        if only_established:
            argmin = np.argmin(distances_established)
            if distances_established[argmin] < threshold:
                return self.clusters[argmin].id
            else:
                return -1
        else:
            if prefer_established:
                argmin = np.argmin(distances_established)
                if distances_established[argmin] < threshold:
                    return self.clusters[argmin].id
                else:
                    argmin_outlier = np.argmin(distances_outlier)
                    if distances_outlier[argmin_outlier] < threshold:
                        return self.outlier_clusters[argmin_outlier].id
                    else:
                        return -1
            else:
                distances = distances_established + distances_outlier
                argmin = np.argmin(distances)
                if argmin < len(distances_established):
                    if distances_established[argmin] < threshold:
                        return self.clusters[argmin].id
                    else:
                        return -1
                else:
                    argmin_outlier = argmin - len(distances_established)
                    if distances_outlier[argmin_outlier] < threshold:
                        return self.outlier_clusters[argmin_outlier].id
                    else:
                        return -1
                    
    def purge_outliers(self, min_samples: int = -1) -> None:
        """ Purge the outlier clusters

        :param min_samples: Samples with fewer than this number of samples are removed from the outlier clusters. -1 to remove all outlier clusters.

        Removes all outlier clusters from the model.
        """
        if min_samples < 0:
            self.outlier_clusters = []
        else:
            self.outlier_clusters = [cluster for cluster in self.outlier_clusters if cluster.number_of_points >= min_samples]

    def calculate_distances(self, sample: np.ndarray) -> np.ndarray:
        """ Calculate the distance of the sample to each cluster

        :param sample: Sample to be compared to the clusters
        :return: Array of distances to all the clusters
        """
        return np.array([cluster.calculate_distance(sample) for cluster in self.clusters])

    def get_prototypes(self) -> list[np.ndarray]:
        """ Get the prototypes of all the clusters

        :return: List of prototypes of all the clusters
        """
        return [cluster.prototype for cluster in self.clusters]
    
    def get_n_clusters(self)->int:
        """ Returns the number of established clusters in the model
        
        :return: Number of established clusters in the model
        """
        return len(self.clusters)

    def get_n_outliers(self)->int:
        """ Returns the number of outlier clusters in the model
        
        :return: Number of outlier clusters in the model
        """
        return len(self.outlier_clusters)
    

    def __getstate__(self) -> dict:
        """ Get the state of the object for pickling

        :return: State of the object
        """
        state = self.__dict__.copy()
        # Remove the generator from the state
        del state['cluster_generator']
        return state
    

    def __setstate__(self, state: dict) -> None:
        """ Set the state of the object for unpickling

        :param state: State of the object
        """
        self.__dict__.update(state)
        # Recreate the generator
        self.cluster_generator = self.get_cluster_id()
