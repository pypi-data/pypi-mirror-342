import numpy as np

from segtree._widget import (
    individual_tree
)

import numpy as np
from PIL import Image
import os

from segtree.utils import get_base_dir  # Assure-toi que c'est bien importable
from napari.types import ImageData, LabelsData

def generate_fake_image(height=256, width=256):
    # Génère une image RGB aléatoire
    return np.random.randint(0, 255, (height, width, 3), dtype=np.uint8)

def generate_fake_label(height=256, width=256):
    # Crée un masque de labels fictif avec deux objets
    mask = np.zeros((height, width), dtype=np.uint8)
    mask[50:100, 50:100] = 1
    return mask

def get_er(*args, **kwargs):
    er_func = individual_tree()
    return er_func(*args, **kwargs)

def test_individual_tree_single_image():
    rgb_data = ImageData (generate_fake_image())
    trunk_data = LabelsData(generate_fake_label())
    
    print("Testing single RGB image with trunk mask...")
    output = get_er(rgb_data, trunk_data)
    # output = individual_tree(rgb_data=rgb_data, trunk_data=trunk_data)
    assert output.shape == trunk_data.shape
    print("Output shape:", output.shape)
    print("Unique labels in output:", np.unique(output))

def test_individual_tree_without_trunk():
    rgb_data = ImageData(generate_fake_image())
    trunk_data = None

    print("Testing single RGB image without trunk mask...")
    output = get_er(rgb_data, trunk_data)
    # output = individual_tree(rgb_data=rgb_data, trunk_data=trunk_data)
    print("Output shape:", output.shape)
    print("Unique labels in output:", np.unique(output))

def test_individual_tree_batch():
    rgb_data = ImageData(np.stack([generate_fake_image() for _ in range(4)]))
    trunk_data = LabelsData(np.stack([generate_fake_label() for _ in range(4)]))

    print("Testing batch of RGB images with masks...")
    output = get_er(rgb_data, trunk_data)
    # output = individual_tree(rgb_data=rgb_data, trunk_data=trunk_data)
    assert output.shape == trunk_data.shape
    print("Batch output shape:", output.shape)
    print("Unique labels in output (per frame):")
    for i in range(output.shape[0]):
        print(f"  Frame {i}: {np.unique(output[i])}")

if __name__ == "__main__":
    test_individual_tree_single_image()
    test_individual_tree_without_trunk()
    test_individual_tree_batch()
