import requests
from io import BytesIO
from zipfile import ZipFile
import os
import datetime
import pickle as pkl
import numpy as np


def download_industrial_dataset(data_folder: str, make_dir: bool = True, skip_if_exists: bool = True) -> None:
    """
    Helper function to dowload the industrial dataset to the specified folder. If the folder is empty, the dataset will
    not be downloaded.

    Upon download, the dataset will be unzipped to the specified folder.
    :param data_folder: Target folder for the dataset
    :param make_dir: Should directory be created if it does not exist?
    :param skip_if_exists: Should skip download if the folder is not empty?
    :return: None
    """
    # URL taken from https://data.mendeley.com/datasets/ypzswhhzh9/2 - see link under "Download All" button.
    dataset_url = "https://prod-dcd-datasets-cache-zipfiles.s3.eu-west-1.amazonaws.com/ypzswhhzh9-2.zip"

    if not os.path.exists(data_folder):
        if not make_dir:
            raise FileNotFoundError("Dataset folder does not exist")
        os.makedirs(data_folder)

    if not os.path.isdir(data_folder):
        raise ValueError("Path supplied is not a directory")

    if len(os.listdir(data_folder)) > 0:
        if skip_if_exists:
            print("Supplied folder is not empty. Skipping dataset download")
            return
        raise FileExistsError("Supplied folder is not empty")
    print("Starting download of dataset")
    tic = datetime.datetime.now()
    response = requests.get(dataset_url)
    print(f"Download complete, took {(datetime.datetime.now() - tic).total_seconds():.1f}s")
    ZipFile(BytesIO(response.content)).extractall(data_folder)
    print(f"Dataset unzipped to {os.path.abspath(data_folder)}")


def load_industrial_dataset(folder: str, download: bool = True, make_dir: bool = True) -> tuple[dict, dict]:
    """ Helper function to load the industrial dataset as a tuple of two dictionaries, one for pressure and one for
    current. Each dictionary contains data and labels keys. Data is a list of numpy arrays, each representing a
    segment of the signal. Labels is a list of integers, each representing a class of the segment.

    :param folder: The folder where the dataset is stored
    :param download: Should try to download the dataset?
    :param make_dir: Should create the directory if it does not exist?
    :return: A tuple of two dictionaries, one for pressure and one for current.
    """
    if download:
        download_industrial_dataset(folder, make_dir=make_dir, skip_if_exists=True)

    suffix: str = os.path.join("Pneumatic Pressure and Electrical Current Time Series in Manufacturing", "Pickle")

    with open(os.path.join(folder, suffix, 'segmented_pressure.pkl'), 'rb') as f:
        pressure = pkl.load(f)

    with open(os.path.join(folder, suffix, "segmented_current.pkl"), 'rb') as f:
        current = pkl.load(f)

    return pressure, current


def get_industrial_data_grouped_by_class(download: bool = True,
                                         folder: str = "Data",
                                         min_samples_per_class: int = 5,
                                         min_sample_length: int = 11,
                                         max_sample_length: int = 600) -> tuple[
    list[list[np.ndarray]], list[list[np.ndarray]]]:
    """ Helper function to load the industrial dataset and group the segments by class. The function will return two
    lists of lists (one for pressure, one for current), where each inner list contains segments of the same class.

    :param download: Should try to download the dataset?
    :param folder: The folder where the dataset is stored
    :param min_samples_per_class: Minimum number of samples per class. Classes with fewer samples will be discarded.
    :param min_sample_length: Minimum length of a sample. Shorter samples will be discarded.
    :param max_sample_length: Maximum length of a sample. Longer samples will be discarded.
    :return: Two lists of lists, where each inner list contains segments of the same class. First list is for pressure,
    second for current.
    """

    pressure, current = load_industrial_dataset(folder=folder, download=download)
    datasets_dict: dict[int, list[np.ndarray]] = {
        state: [series.to_numpy() for i, series in enumerate(pressure['data']) if
                pressure['labels'][i] == state and len(series) >= min_sample_length and len(
                    series) <= max_sample_length] for state in np.unique(pressure['labels'])}
    datasets_dict = {k: v for k, v in datasets_dict.items() if min_samples_per_class < len(v)}
    datasets_pressure = [v for k, v in datasets_dict.items()]

    datasets_dict: dict[int, list[np.ndarray]] = {
        state: [series.to_numpy() for i, series in enumerate(current['data']) if
                current['labels'][i] == state and len(series) >= min_sample_length and len(series) <= max_sample_length]
        for state in np.unique(current['labels'])}
    datasets_dict = {k: v for k, v in datasets_dict.items() if min_samples_per_class < len(v)}
    datasets_current = [v for k, v in datasets_dict.items()]

    return datasets_pressure, datasets_current


def get_industrial_unlabeled(download: bool = True,
                             folder: str = "Data",
                             min_sample_length: int = 11,
                             max_sample_length: int = 600) -> tuple[list[np.ndarray], list[np.ndarray]]:
    """ Helper function to load the industrial dataset and group the segments by class. The function will return two
    lists (one for pressure, one for current)

    :param download: Should try to download the dataset?
    :param folder: The folder where the dataset is stored
    :param min_samples_per_class: Minimum number of samples per class. Classes with fewer samples will be discarded.
    :param min_sample_length: Minimum length of a sample. Shorter samples will be discarded.
    :param max_sample_length: Maximum length of a sample. Longer samples will be discarded.
    :return: Two lists, one for pressure, second for current.
    """

    pressure, current = load_industrial_dataset(folder=folder, download=download)

    pressure_return = [x.values for x in pressure['data'] if
                       len(x) >= min_sample_length and len(x) <= max_sample_length]
    current_return = [x.values for x in current['data'] if len(x) >= min_sample_length and len(x) <= max_sample_length]

    return pressure_return, current_return

def get_industrial_labeled(download: bool = True,
                             folder: str = "Data",
                             min_sample_length: int = 11,
                             max_sample_length: int = 600,
                             min_samples_per_class: int = 1) -> tuple[list[np.ndarray], list[np.ndarray], list[int]]:
    """ Helper function to load the industrial dataset and group the segments by class. The function will return two
    lists (one for pressure, one for current)

    :param download: Should try to download the dataset?
    :param folder: The folder where the dataset is stored
    :param min_samples_per_class: Minimum number of samples per class. Classes with fewer samples will be discarded.
    :param min_sample_length: Minimum length of a sample. Shorter samples will be discarded.
    :param max_sample_length: Maximum length of a sample. Longer samples will be discarded.
    :param min_samples_per_class: Minimum number of samples per class. Classes with fewer samples will be discarded.
    :return: Two lists, one for pressure, second for current.
    """

    pressure, current = load_industrial_dataset(folder=folder, download=download)

    pressure_return = [x.values for x in pressure['data'] if
                       len(x) >= min_sample_length and len(x) <= max_sample_length]
    current_return = [x.values for x in current['data'] if len(x) >= min_sample_length and len(x) <= max_sample_length]

    labels = [x for i, x in enumerate(pressure['labels']) if len(pressure['data'][i]) >= min_sample_length and len(pressure['data'][i]) <= max_sample_length]

    if min_samples_per_class <= 1:
        return pressure_return, current_return, labels
    
    class_sizes = [labels.count(x) for x in np.unique(labels)]
    excluded_classes = [x for i, x in enumerate(np.unique(labels)) if class_sizes[i] < min_samples_per_class]

    pressure_return = [x for i, x in enumerate(pressure_return) if labels[i] not in excluded_classes]
    current_return = [x for i, x in enumerate(current_return) if labels[i] not in excluded_classes]
    labels = [x for x in labels if x not in excluded_classes]   

    return pressure_return, current_return, labels