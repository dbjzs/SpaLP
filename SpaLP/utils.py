import anndata
import numpy as np
from scipy.spatial import cKDTree
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import random
def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.backends.cudnn.deterministic = True 
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.benchmark = False

class Graph:
    def __init__(self, features, neighbor_idx, batches=None):
        """
        Graph data structure to store coordinates, features, and neighbor indices.

        Args:
            features (torch.Tensor): Features, shape (N, C).
            neighbor_idx (torch.Tensor): Neighbor indices, shape (N, k).
            batches (list, optional): Preprocessed batch data for training. Defaults to None.
        """
        self.features = features
        self.neighbor_idx = neighbor_idx
        self.batches = batches 
        
    def get_node(self, node_idx):
        return {
            "features": self.features[node_idx], 
            "neighbor_idx": self.neighbor_idx[node_idx]
        }

def build_neighbor_idx(coords, k):
    if not isinstance(coords, np.ndarray):
        coords = np.array(coords)
    N = coords.shape[0]
    tree = cKDTree(coords)
    _, indices = tree.query(coords, k=k, workers=-1)  # indices: (N, k)
    indices = indices[:, 1:]
    return torch.tensor(indices, dtype=torch.long)

def prepare_inputs(adata,k, device):
    features = adata.obsm['feat']
    if hasattr(features, 'toarray'):
        features = features.toarray()
    coords = adata.obsm['spatial']
    features = torch.tensor(features, dtype=torch.float32)  # (N, C) 
    neighbor_idx = build_neighbor_idx(coords, k)
    
    features = features.to(device)
    neighbor_idx = neighbor_idx.to(device)
    
    return Graph(features, neighbor_idx)


def prepare_inputs_batch(adata, k, batch_size):
    features = adata.obsm['feat']
    if hasattr(features, 'toarray'):
        features = features.toarray()
    coords = adata.obsm['spatial']

    features = torch.tensor(features, dtype=torch.float32).cpu()
    neighbor_idx = build_neighbor_idx(coords, k+1).cpu()

    N = features.shape[0]
    batch_starts = list(range(0, N, batch_size))

    batches = []
    for start in batch_starts:
        end = min(start + batch_size, N)
        bs = end - start

        batch_idx = torch.arange(start, end, device='cpu')
        batch_features = features[batch_idx]
        batch_neighbor_global = neighbor_idx[batch_idx]
        batch_neighbor_local = batch_neighbor_global - start

        valid_mask = (batch_neighbor_local >= 0) & (batch_neighbor_local < bs)
        batch_neighbor_local[~valid_mask] = -1

        batches.append({
            'features': batch_features,          
            'neighbor_local': batch_neighbor_local
        })

    return Graph(features, neighbor_idx, batches=batches)



    


default_color_dict = {
    "0": "#66C5CC",
    "1": "#F6CF71",
    "2": "#F89C74",
    "3": "#DCB0F2",
    "4": "#87C55F",
    "5": "#9EB9F3",
    "6": "#FE88B1",
    "7": "#C9DB74",
    "8": "#8BE0A4",
    "9": "#B497E7",
    "10": "#D3B484",
    "11": "#B3B3B3",
    "12": "#276A8C", # Royal Blue
    "13": "#DAB6C4", # Pink
    "14": "#C38D9E", # Mauve-Pink
    "15": "#9D88A2", # Mauve
    "16": "#FF4D4D", # Light Red
    "17": "#9B4DCA", # Lavender-Purple
    "18": "#FF9CDA", # Bright Pink
    "19": "#FF69B4", # Hot Pink
    "20": "#FF00FF", # Magenta
    "21": "#DA70D6", # Orchid
    "22": "#BA55D3", # Medium Orchid
    "23": "#8A2BE2", # Blue Violet
    "24": "#9370DB", # Medium Purple
    "25": "#7B68EE", # Medium Slate Blue
    "26": "#4169E1", # Royal Blue
    "27": "#FF8C8C", # Salmon Pink
    "28": "#FFAA80", # Light Coral
    "29": "#48D1CC", # Medium Turquoise
    "30": "#40E0D0", # Turquoise
    "31": "#00FF00", # Lime
    "32": "#7FFF00", # Chartreuse
    "33": "#ADFF2F", # Green Yellow
    "34": "#32CD32", # Lime Green
    "35": "#228B22", # Forest Green
    "36": "#FFD8B8", # Peach
    "37": "#008080", # Teal
    "38": "#20B2AA", # Light Sea Green
    "39": "#00FFFF", # Cyan
    "40": "#00BFFF", # Deep Sky Blue
    "41": "#4169E1", # Royal Blue
    "42": "#0000CD", # Medium Blue
    "43": "#00008B", # Dark Blue
    "44": "#8B008B", # Dark Magenta
    "45": "#FF1493", # Deep Pink
    "46": "#FF4500", # Orange Red
    "47": "#006400", # Dark Green
    "48": "#FF6347", # Tomato
    "49": "#FF7F50", # Coral
    "50": "#CD5C5C", # Indian Red
    "51": "#B22222", # Fire Brick
    "52": "#FFB83F",  # Light Orange
    "53": "#8B0000", # Dark Red
    "54": "#D2691E", # Chocolate
    "55": "#A0522D", # Sienna
    "56": "#800000", # Maroon
    "57": "#808080", # Gray
    "58": "#A9A9A9", # Dark Gray
    "59": "#C0C0C0", # Silver
    "60": "#9DD84A",
    "61": "#F5F5F5", # White Smoke
    "62": "#F17171", # Light Red
    "63": "#000000", # Black
    "64": "#FF8C42", # Tangerine
    "65": "#F9A11F", # Bright Orange-Yellow
    "66": "#FACC15", # Golden Yellow
    "67": "#E2E062", # Pale Lime
    "68": "#BADE92", # Soft Lime
    "69": "#70C1B3", # Greenish-Blue
    "70": "#41B3A3", # Turquoise
    "71": "#5EAAA8", # Gray-Green
    "72": "#72B01D", # Chartreuse
    "73": "#9CD08F", # Light Green
    "74": "#8EBA43", # Olive Green
    "75": "#FAC8C3", # Light Pink
    "76": "#E27D60", # Dark Salmon
    "77": "#C38D9E", # Mauve-Pink
    "78": "#937D64", # Light Brown
    "79": "#B1C1CC", # Light Blue-Gray
    "80": "#88A0A8", # Gray-Blue-Green
    "81": "#4E598C", # Dark Blue-Purple
    "82": "#4B4E6D", # Dark Gray-Blue
    "83": "#8E9AAF", # Light Blue-Grey
    "84": "#C0D6DF", # Pale Blue-Grey
    "85": "#97C1A9", # Blue-Green
    "86": "#4C6E5D", # Dark Green
    "87": "#95B9C7", # Pale Blue-Green
    "88": "#C1D5E0", # Pale Gray-Blue
    "89": "#ECDB54", # Bright Yellow
    "90": "#E89B3B", # Bright Orange
    "91": "#CE5A57", # Deep Red
    "92": "#C3525A", # Dark Red
}

def create_new_color_dict(
        adata,
        cat_key,
        color_palette="default",
        overwrite_color_dict={"-1" : "#E1D9D1"},
        skip_default_colors=0):
    """
    Create a dictionary of color hexcodes for a specified category.

    Parameters
    ----------
    adata:
        AnnData object.
    cat_key:
        Key in ´adata.obs´ where the categories are stored for which color
        hexcodes will be created.
    color_palette:
        Type of color palette.
    overwrite_color_dict:
        Dictionary with overwrite values that will take precedence over the
        automatically created dictionary.
    skip_default_colors:
        Number of colors to skip from the default color dict.

    Returns
    ----------
    new_color_dict:
        The color dictionary with a hexcode for each category.
    """
    new_categories = adata.obs[cat_key].unique().tolist()
    if color_palette == "cell_type_30":
        # https://github.com/scverse/scanpy/blob/master/scanpy/plotting/palettes.py#L40
        new_color_dict = {key: value for key, value in zip(
            new_categories,
            ["#023fa5",
             "#7d87b9",
             "#bec1d4",
             "#d6bcc0",
             "#bb7784",
             "#8e063b",
             "#4a6fe3",
             "#8595e1",
             "#b5bbe3",
             "#e6afb9",
             "#e07b91",
             "#d33f6a",
             "#11c638",
             "#8dd593",
             "#c6dec7",
             "#ead3c6",
             "#f0b98d",
             "#ef9708",
             "#0fcfc0",
             "#9cded6",
             "#d5eae7",
             "#f3e1eb",
             "#f6c4e1",
             "#f79cd4",
             '#7f7f7f',
             "#c7c7c7",
             "#1CE6FF",
             "#336600"])}
    elif color_palette == "cell_type_20":
        # https://github.com/vega/vega/wiki/Scales#scale-range-literals (some adjusted)
        new_color_dict = {key: value for key, value in zip(
            new_categories,
            ['#1f77b4',
             '#ff7f0e',
             '#279e68',
             '#d62728',
             '#aa40fc',
             '#8c564b',
             '#e377c2',
             '#b5bd61',
             '#17becf',
             '#aec7e8',
             '#ffbb78',
             '#98df8a',
             '#ff9896',
             '#c5b0d5',
             '#c49c94',
             '#f7b6d2',
             '#dbdb8d',
             '#9edae5',
             '#ad494a',
             '#8c6d31'])}
    elif color_palette == "cell_type_10":
        # scanpy vega10
        new_color_dict = {key: value for key, value in zip(
            new_categories,
            ['#7f7f7f',
             '#ff7f0e',
             '#279e68',
             '#e377c2',
             '#17becf',
             '#8c564b',
             '#d62728',
             '#1f77b4',
             '#b5bd61',
             '#aa40fc'])}
    elif color_palette == "batch":
        # sns.color_palette("colorblind").as_hex()
        new_color_dict = {key: value for key, value in zip(
            new_categories,
            ['#0173b2', '#d55e00', '#ece133', '#ca9161', '#fbafe4',
             '#949494', '#de8f05', '#029e73', '#cc78bc', '#56b4e9',
             '#F0F8FF', '#FAEBD7', '#00FFFF', '#7FFFD4', '#F0FFFF',
             '#F5F5DC', '#FFE4C4', '#000000', '#FFEBCD', '#0000FF',
             '#8A2BE2', '#A52A2A', '#DEB887', '#5F9EA0', '#7FFF00',
             '#D2691E', '#FF7F50', '#6495ED', '#FFF8DC', '#DC143C'])}
    elif color_palette == "default":
        new_color_dict = {key: value for key, value in zip(new_categories, list(default_color_dict.values())[skip_default_colors:])}
    for key, val in overwrite_color_dict.items():
        new_color_dict[key] = val
    return new_color_dict


from sklearn.preprocessing import normalize
def transfer_labels_by_cosine(pre_adata, new_adata, label_key="Compartment", embedding_key="SpaLP"):
    X_ref = pre_adata.obsm[embedding_key]
    X_new = new_adata.obsm[embedding_key]
    
    labels_ref = pre_adata.obs[label_key].values
    
    X_ref_norm = normalize(X_ref, axis=1)
    X_new_norm = normalize(X_new, axis=1)
    cosine_sim = X_new_norm @ X_ref_norm.T
    
    nearest_idx = cosine_sim.argmax(axis=1)
    
    new_adata.obs["Transfer_label"] = labels_ref[nearest_idx]
    new_adata.obs["Cosine_confidence"] = cosine_sim.max(axis=1)
    
    return new_adata