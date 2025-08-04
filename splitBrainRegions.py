import pandas as pd

def splitBrainRegions() -> str:
    dataset = pd.read_excel('data/dataset_neuroscience_vo.xlsx', sheet_name='c-Fos-counts')
    brain_regions = dataset.iloc[:, 0].astype(str).tolist()
    regions_str = ", ".join(brain_regions)
    return regions_str

# Exemple d'utilisation
try:
    regions = splitBrainRegions()
    print("Abréviations des régions :")
    print(regions)
except Exception as e:
    print(f"Erreur : {str(e)}")