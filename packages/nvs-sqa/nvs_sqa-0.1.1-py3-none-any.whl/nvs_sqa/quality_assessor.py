import os
import glob
import torch
import numpy as np
from .utils import load_model, load_regression_model

class QualityAssessor:
    """
    A wrapper class for loading the encoder and regression model,
    generating quality features from image view paths, and computing quality scores.
    """
    def __init__(self, device=None):
        self.device = device if device else torch.device("cuda" if torch.cuda.is_available() else "cpu")
        # Load the encoder and regression model separately
        self.encoder = load_model(self.device)
        self.encoder.eval()
        self.regressor = load_regression_model()

    def predict_features_from_views(self, view_paths, verbose=False):
        """
        Given a list of image file paths, predict features using the encoder.
        Args:
            view_paths (list): A list of image file paths.
            verbose (bool): Flag for printing additional info.
        Returns:
            np.ndarray: Predicted features in numpy array format.
        """
        if verbose:
            print("Predicting features for provided view paths...")
        with torch.no_grad():
            feats = self.encoder.predict_features_from_view_paths(view_paths, self.device)
        return feats.cpu().numpy()

    def generate_quality_features(self, eval_folder, save_path=None, verbose=False):
        """
        Process each NSS folder in the evaluation folder, predict features,
        and save the results to a .npz file.
        
        Args:
            eval_folder (str): Path where evaluation folders (NSS folders) are located.
            save_path (str, optional): Full path to save the feature file. If not provided,
                                       defaults to a file named "output_features.npz" inside eval_folder.
            verbose (bool): Flag for printing additional info.
        
        Returns:
            tuple(dict, str): Dictionary of {nss_name: features} and the path where features were saved.
        """
        if save_path is None:
            save_path = os.path.join(eval_folder, "output_features.npz")
            if verbose:
                print(f"No save_path provided. Using default: {save_path}")

        all_feats = {}
        nss_names = sorted([name for name in os.listdir(eval_folder) 
                            if os.path.isdir(os.path.join(eval_folder, name))])
        if verbose:
            print(f"Found NSS folders: {nss_names}")
        for name in nss_names:
            nss_folder = os.path.join(eval_folder, name)
            view_paths = glob.glob(os.path.join(nss_folder, "*.*"))
            # Only process common image formats (case-insensitive)
            view_paths = sorted([vp for vp in view_paths if vp.split(".")[-1].lower() in ["png", "jpg", "jpeg"]])
            if verbose:
                print(f"Processing folder: {nss_folder} with {len(view_paths)} valid image(s)")
            if view_paths:
                features = self.predict_features_from_views(view_paths, verbose)
                all_feats[name] = features

        np.savez(save_path, **all_feats)
        if verbose:
            print(f"***** Quality features were saved in {save_path}")
        return all_feats, save_path

    def generate_quality_scores(self, all_feats, verbose=False):
        """
        Compute a quality score for each NSS by applying ridge regression
        on the collected feature representations.
        
        Args:
            all_feats (dict): Dictionary of {nss_name: features}.
            verbose (bool): Flag for printing additional info.
        
        Returns:
            dict: Dictionary of {nss_name: quality score}
        """
        if verbose:
            print("========= Calculating Quality Scores ==========")
            print("Note: JOD scores are primarily negative; higher values denote better quality.")
        quality_scores = {}
        # Collect features per NSS in a list for regression prediction
        feats_list = [all_feats[name] for name in all_feats]
        preds = self.regressor.predict(feats_list)
        if verbose:
            print("========= Quality Score Results ==========")
        for idx, nss_name in enumerate(all_feats):
            if verbose:
                print(f"{nss_name}: {preds[idx]:.4f}")
            quality_scores[nss_name] = preds[idx]
        return quality_scores
