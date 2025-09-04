import pandas as pd
import numpy as np
import pickle

DATASET_PATH1 = "ssh/dataset/dataset_neuroscience_1.xlsx"
DATASET_PATH2 = "ssh/dataset/dataset_neuroscience_2.xlsx"
DATASET_PATH3 = "ssh/dataset/dataset_neuroscience_3.xlsx"
DATASET_PATH4 = "ssh/dataset/dataset_neuroscience_4.xlsx"
DATASET_PATH5 = "ssh/dataset/dataset_neuroscience_vo.xlsx"

OUTPUT_PATH = "ssh/data/data.pkl"


def load_data_from_dataset():
    # Load datasets

    # Dataset 1 : 20 regions and 2 groups (16 mice)
    dataset1 = pd.read_excel(DATASET_PATH1)

    # Dataset 2 : 40 regions and 4 groups (32 mice)
    dataset2 = pd.read_excel(DATASET_PATH2)

    # Dataset 3 : 80 regions and 4 groups (32 mice)
    dataset3 = pd.read_excel(DATASET_PATH3)

    # Dataset 4 : 160 regions and 6 groups (48 mice)
    dataset4 = pd.read_excel(DATASET_PATH4)

    # Dataset 5 : 314 regions and 8 groups (64 mice)
    dataset5 = pd.read_excel(DATASET_PATH5)

    return dataset1, dataset2, dataset3, dataset4, dataset5


def copy_dataset(dataset1, dataset2, dataset3, dataset4, dataset5):
    # Remove last row (male or female indicator)

    data_clean1 = dataset1.iloc[:-1].copy()
    data_clean2 = dataset2.iloc[:-1].copy()
    data_clean3 = dataset3.iloc[:-1].copy()
    data_clean4 = dataset4.iloc[:-1].copy()
    data_clean5 = dataset5.iloc[:-1].copy()

    return data_clean1, data_clean2, data_clean3, data_clean4, data_clean5


def convert_type_data(data_clean1, data_clean2, data_clean3, data_clean4, data_clean5):
    # Seperate data and metadata

    metadata1 = data_clean1[['abbreviation', 'region name', 'brain area']]
    count_data1 = data_clean1.iloc[:, 3:]

    metadata2 = data_clean2[['abbreviation', 'region name', 'brain area']]
    count_data2 = data_clean2.iloc[:, 3:]

    metadata3 = data_clean3[['abbreviation', 'region name', 'brain area']]
    count_data3 = data_clean3.iloc[:, 3:]

    metadata4 = data_clean4[['abbreviation', 'region name', 'brain area']]
    count_data4 = data_clean4.iloc[:, 3:]

    metadata5 = data_clean5[['abbreviation', 'region name', 'brain area']]
    count_data5 = data_clean5.iloc[:, 3:]

    # Convert large format to long format

    # Dataset 1
    counts1, region_id1, group_id1 = [], [], []

    # Dataset 2
    counts2, region_id2, group_id2 = [], [], []

    # Dataset 3
    counts3, region_id3, group_id3 = [], [], []

    # Dataset 4
    counts4, region_id4, group_id4 = [], [], []

    # Dataset 5
    counts5, region_id5, group_id5 = [], [], []

