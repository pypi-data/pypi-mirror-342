import torch
import glob
import os
from . import models
from .models import sequence_models
import pickle
import importlib.resources as pkg_resources
import sys
import pathlib


version = "v0.0.1"
# Define a function to get the path to resources that works in both dev and installed modes
def get_resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        # If the application is run as a bundle
        base_path = pathlib.Path(sys._MEIPASS)
    else:
        # Get the directory where this file is located
        base_path = pathlib.Path(__file__).parent
    
    return str(base_path / relative_path)

model_save_folder = get_resource_path(f"checkpoints/{version}/models")
epo_offset=100

def load_model(device):
    encoder_config_path = find_first_json_with_prefix(model_save_folder, "SeqModel")

    encoder = sequence_models.EfficientSequenceModel.load_from_config(encoder_config_path).to(device)

    encoder_path = os.path.join(model_save_folder, f"{encoder.model_name}_{epo_offset}.pth") 
    encoder.load_state_dict(torch.load(encoder_path, map_location=device))

    print(f"Loaded model from: {encoder_path}")

    return encoder


def load_regression_model():
    regr_save_folder = model_save_folder.replace("models", "regr")

    regr_save_path = os.path.join(regr_save_folder, "linear_regr.pkl")
    with open(regr_save_path, 'rb') as f:
        regr = pickle.load(f)
    
    return regr


def find_first_json_with_prefix(folder_path, prefix):
    """
    Find the first JSON file in a folder that starts with a given prefix.

    Args:
    - folder_path (str): Path to the folder to search in.
    - prefix (str): The prefix of the file name.

    Returns:
    - str: The path to the first matching JSON file, or None if no match is found.
    """
    search_pattern = os.path.join(folder_path, f"{prefix}*.json")
    matching_files = glob.glob(search_pattern)

    if matching_files:
        return matching_files[0]  # Return the first matching file
    else:
        return None

