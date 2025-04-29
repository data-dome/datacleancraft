# """
# Module: anomaly_detector
# Detects anomalies in numeric datasets using a simple Autoencoder.
# """

# import numpy as np
# import pandas as pd
# import torch
# from datacleancraft.models.autoencoder_loader import SimpleAutoencoder, load_autoencoder
# from datacleancraft.utils.error_handler import handle_exception

# class AnomalyDetector:
#     def __init__(self, threshold: float = 0.1):
#         """
#         Initialize the anomaly detector.

#         Args:
#             threshold (float): Reconstruction error threshold to mark anomalies.
#         """
#         self.threshold = threshold
#         self.model = None
#         self.input_dim = None

#     @handle_exception
#     def detect_anomalies(self, df: pd.DataFrame) -> pd.DataFrame:
#         """
#         Detect anomalies and return anomaly scores.

#         Args:
#             df (pd.DataFrame): Numeric DataFrame.

#         Returns:
#             pd.DataFrame: DataFrame with anomaly scores and anomaly flags.
#         """
#         numeric_df = df.select_dtypes(include=[np.number]).dropna()

#         if numeric_df.empty:
#             raise ValueError("No numeric data available for anomaly detection.")

#         self.input_dim = numeric_df.shape[1]
#         self.model = load_autoencoder(self.input_dim)
#         self.model.eval()

#         with torch.no_grad():
#             inputs = torch.tensor(numeric_df.values, dtype=torch.float32)
#             outputs = self.model(inputs)
#             reconstruction_error = torch.mean((outputs - inputs) ** 2, dim=1)
#             anomaly_score = reconstruction_error.numpy()
#             anomalies = anomaly_score > self.threshold

#         result = pd.DataFrame({
#             "anomaly_score": anomaly_score,
#             "is_anomaly": anomalies
#         }, index=numeric_df.index)

#         return result
import numpy as np
import pandas as pd
import torch
from datacleancraft.models.autoencoder_loader import load_autoencoder
from datacleancraft.utils.error_handler import handle_exception

class AnomalyDetector:
    def __init__(self, threshold: float = 0.1):
        """
        Initialize the anomaly detector.

        Args:
            threshold (float): Reconstruction error threshold to mark anomalies.
        """
        self.threshold = threshold
        self.model = None
        self.input_dim = None

    @handle_exception
    def detect_anomalies(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Detect anomalies and return anomaly scores.

        Args:
            df (pd.DataFrame): Numeric DataFrame.

        Returns:
            pd.DataFrame: DataFrame with anomaly scores and anomaly flags.
        """
        # Ensure the dataframe has numeric columns
        numeric_df = df.select_dtypes(include=[np.number]).dropna()

        if numeric_df.empty:
            raise ValueError("No numeric data available for anomaly detection.")

        self.input_dim = numeric_df.shape[1]

        # Load the autoencoder model only if it's not loaded yet
        if self.model is None:
            print(f"Loading autoencoder model for input dimension {self.input_dim}")
            self.model = load_autoencoder(self.input_dim)
            self.model.eval()  # Set the model to evaluation mode

        # Convert the dataframe to a tensor for inference
        with torch.no_grad():
            inputs = torch.tensor(numeric_df.values, dtype=torch.float32)
            outputs = self.model(inputs)
            reconstruction_error = torch.mean((outputs - inputs) ** 2, dim=1)
            anomaly_score = reconstruction_error.numpy()

            # Detect anomalies based on the reconstruction error
            anomalies = anomaly_score > self.threshold

        # Return the result with anomaly score and flags
        result = pd.DataFrame({
            "anomaly_score": anomaly_score,
            "is_anomaly": anomalies
        }, index=numeric_df.index)

        return result
