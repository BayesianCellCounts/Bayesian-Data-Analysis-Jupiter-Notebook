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

    groups1 = list(set(col.split(' ')[0] for col in count_data1.columns))
    group1_map = {g: i for i, g in enumerate(groups1)}

    for r, region in enumerate(metadata1['abbreviation']):
        for c, col in enumerate(count_data1.columns):
            group = col.split(' ')[0]
            counts1.append(count_data1.iloc[r, c])
            region_id1.append(r)
            group_id1.append(group1_map[group])

    # Dataset 2
    counts2, region_id2, group_id2 = [], [], []

    groups2 = list(set(col.split(' ')[0] for col in count_data2.columns))
    group2_map = {g: i for i, g in enumerate(groups2)}

    for r, region in enumerate(metadata2['abbreviation']):
        for c, col in enumerate(count_data2.columns):
            group = col.split(' ')[0]
            counts2.append(count_data2.iloc[r, c])
            region_id2.append(r)
            group_id2.append(group2_map[group])

    # Dataset 3
    counts3, region_id3, group_id3 = [], [], []

    groups3 = list(set(col.split(' ')[0] for col in count_data3.columns))
    group3_map = {g: i for i, g in enumerate(groups3)}

    for r, region in enumerate(metadata3['abbreviation']):
        for c, col in enumerate(count_data3.columns):
            group = col.split(' ')[0]
            counts3.append(count_data3.iloc[r, c])
            region_id3.append(r)
            group_id3.append(group3_map[group])

    # Dataset 4
    counts4, region_id4, group_id4 = [], [], []

    groups4 = list(set(col.split(' ')[0] for col in count_data4.columns))
    group4_map = {g: i for i, g in enumerate(groups4)}

    for r, region in enumerate(metadata4['abbreviation']):
        for c, col in enumerate(count_data4.columns):
            group = col.split(' ')[0]
            counts4.append(count_data4.iloc[r, c])
            region_id4.append(r)
            group_id4.append(group4_map[group])

    # Dataset 5
    counts5, region_id5, group_id5 = [], [], []

    groups5 = list(set(col.split(' ')[0] for col in count_data5.columns))
    group5_map = {g: i for i, g in enumerate(groups5)}

    for r, region in enumerate(metadata5['abbreviation']):
        for c, col in enumerate(count_data5.columns):
            group = col.split(' ')[0]
            counts5.append(count_data5.iloc[r, c])
            region_id5.append(r)
            group_id5.append(group5_map[group])

    return counts1, region_id1, group_id1, counts2, region_id2, group_id2, counts3, region_id3, group_id3, counts4, region_id4, group_id4, counts5, region_id5, group_id5


def prepare_data_dicts(counts1, region_id1, group_id1, counts2, region_id2, group_id2, counts3, region_id3, group_id3,
                       counts4, region_id4, group_id4,
                       counts5, region_id5, group_id5, metadata1, metadata2, metadata3, metadata4, metadata5, groups1,
                       groups2, groups3, groups4, groups5):
    # Prepare data dictionaries
    data1 = {
        'counts': np.array(counts1, dtype=int),
        'region_id': np.array(region_id1),
        'group_id': np.array(group_id1),
        'n_regions': len(metadata1),
        'n_groups': len(groups1),
        'region_names': metadata1['abbreviation'].tolist(),
        'group_names': groups1
    }

    data2 = {
        'counts': np.array(counts2, dtype=int),
        'region_id': np.array(region_id2),
        'group_id': np.array(group_id2),
        'n_regions': len(metadata2),
        'n_groups': len(groups2),
        'region_names': metadata2['abbreviation'].tolist(),
        'group_names': groups2
    }

    data3 = {
        'counts': np.array(counts3, dtype=int),
        'region_id': np.array(region_id3),
        'group_id': np.array(group_id3),
        'n_regions': len(metadata3),
        'n_groups': len(groups3),
        'region_names': metadata3['abbreviation'].tolist(),
        'group_names': groups3
    }

    data4 = {
        'counts': np.array(counts4, dtype=int),
        'region_id': np.array(region_id4),
        'group_id': np.array(group_id4),
        'n_regions': len(metadata4),
        'n_groups': len(groups4),
        'region_names': metadata4['abbreviation'].tolist(),
        'group_names': groups4
    }

    data5 = {
        'counts': np.array(counts5, dtype=int),
        'region_id': np.array(region_id5),
        'group_id': np.array(group_id5),
        'n_regions': len(metadata5),
        'n_groups': len(groups5),
        'region_names': metadata5['abbreviation'].tolist(),
        'group_names': groups5
    }

    return data1, data2, data3, data4, data5


def save_data_to_pickle(data1, data2, data3, data4, data5):
    with open(OUTPUT_PATH, 'wb') as f:
        pickle.dump((data1, data2, data3, data4, data5), f)

    print(f"Data saved to {OUTPUT_PATH}")
    print(f"Regions for dataset 1: {data1['n_regions']} \n"
          f"Groups for dataset 1: {data1['n_groups']} \n"
          f"Observations for dataset 1: {len(data1['counts'])} \n")

    print(f"Regions for dataset 2: {data2['n_regions']} \n"
          f"Groups for dataset 2: {data2['n_groups']} \n"
          f"Observations for dataset 2: {len(data2['counts'])} \n")

    print(f"Regions for dataset 3: {data3['n_regions']} \n"
          f"Groups for dataset 3: {data3['n_groups']} \n"
          f"Observations for dataset 3: {len(data3['counts'])} \n")

    print(f"Regions for dataset 4: {data4['n_regions']} \n"
          f"Groups for dataset 4: {data4['n_groups']} \n"
          f"Observations for dataset 4: {len(data4['counts'])} \n")

    print(f"Regions for dataset 5: {data5['n_regions']} \n"
          f"Groups for dataset 5: {data5['n_groups']} \n"
          f"Observations for dataset 5: {len(data5['counts'])} \n")


if __name__ == "__main__":
    load_data_from_dataset()

    copy_dataset(dataset1, dataset2, dataset3, dataset4, dataset5)

    convert_type_data(data_clean1, data_clean2, data_clean3, data_clean4, data_clean5)

    save_data_to_pickle(data1, data2, data3, data4, data5)