import pandas as pd
import numpy as np
import pickle

DATASET_PATH1 = "dataset_neuroscience_1.xlsx"
DATASET_PATH2 = "dataset_neuroscience_2.xlsx"
DATASET_PATH3 = "dataset_neuroscience_3.xlsx"
DATASET_PATH4 = "dataset_neuroscience_4.xlsx"
DATASET_PATH5 = "dataset_neuroscience_vo.xlsx"

OUTPUT_PATH = "../data/data.pkl"


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

    # Dataset 1, Dataset 2, Dataset 3, Dataset 4, Dataset 5

    results = []
    metadatas = [metadata1, metadata2, metadata3, metadata4, metadata5]
    count_datas = [count_data1, count_data2, count_data3, count_data4, count_data5]

    for i, (metadata, count_data) in enumerate(zip(metadatas, count_datas)):

        counts, region_id, group_id = [], [], []

        groups = list(set(col.split(' ')[0] for col in count_data.columns))

        group_map = {g: j for j, g in enumerate(groups)}

        for r, region in enumerate(metadata['abbreviation']):
            for c, col in enumerate(count_data.columns):
                group = col.split(' ')[0]
                counts.append(count_data.iloc[r, c])
                region_id.append(r)
                group_id.append(group_map[group])

        results.append((counts, region_id, group_id, groups))

    return results, metadatas


def prepare_data_dicts(results, metadatas):
    # Prepare data dictionaries

    data_dicts = []

    for i, ((counts, region_id, group_id, groups), metadata) in enumerate(zip(results, metadatas)):
        data_dict = {
            'counts': np.array(counts, dtype=int),
            'region_id': np.array(region_id),
            'group_id': np.array(group_id),
            'n_regions': len(metadata),
            'n_groups': len(set(group_id)),
            'region_names': metadata['abbreviation'].tolist(),
            'group_names': groups
        }

        data_dicts.append(data_dict)

    return data_dicts


def save_data_to_pickle(data_dicts):
    with open(OUTPUT_PATH, 'wb') as f:
        pickle.dump(tuple(data_dicts), f)

    for i, data in enumerate(data_dicts):
        print(f"Dataset {i + 1}:")
        print(f"  - Régions: {data['n_regions']}")
        print(f"  - Groupes: {data['n_groups']}")
        print(f"  - Observations: {len(data['counts'])}")
        print(f"  - Groupes: {data['group_names']}\n")


def run():
    dataset1, dataset2, dataset3, dataset4, dataset5 = load_data_from_dataset()

    data_clean1, data_clean2, data_clean3, data_clean4, data_clean5 = copy_dataset(dataset1, dataset2, dataset3,
                                                                                   dataset4, dataset5)

    results, metadatas = convert_type_data(data_clean1, data_clean2, data_clean3, data_clean4, data_clean5)

    data_dicts = prepare_data_dicts(results, metadatas)

    save_data_to_pickle(data_dicts)


if __name__ == "__main__":
    run()