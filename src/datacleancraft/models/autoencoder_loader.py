"""
autoencoder_loader.py: Utility for loading and preparing Autoencoder models for anomaly detection.
"""

import torch
import torch.nn as nn
import logging

logger = logging.getLogger(__name__)

class SimpleAutoencoder(nn.Module):
    """
    Basic Autoencoder architecture for structured numeric data.

    Encoder compresses input; Decoder reconstructs it.
    """

    def __init__(self, input_dim: int):
        """
        Initialize the Autoencoder layers.

        Args:
            input_dim (int): Number of features in the input data.
        """
        super(SimpleAutoencoder, self).__init__()

        self.encoder = nn.Sequential(
            nn.Linear(input_dim, input_dim // 2),
            nn.ReLU(),
            nn.Linear(input_dim // 2, input_dim // 4),
            nn.ReLU(),
        )

        self.decoder = nn.Sequential(
            nn.Linear(input_dim // 4, input_dim // 2),
            nn.ReLU(),
            nn.Linear(input_dim // 2, input_dim),
        )

    def forward(self, x):
        """
        Forward pass through the Autoencoder.

        Args:
            x (torch.Tensor): Input batch.

        Returns:
            torch.Tensor: Reconstructed batch.
        """
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded

def load_autoencoder(input_dim: int) -> nn.Module:
    """
    Load a simple untrained Autoencoder model.

    Args:
        input_dim (int): Number of features in the input data.

    Returns:
        nn.Module: SimpleAutoencoder instance.
    """
    try:
        model = SimpleAutoencoder(input_dim)
        logger.info(f"[AutoencoderLoader] Loaded autoencoder with input dimension {input_dim}")
        # Load pre-trained weights if necessary
        #model.load_state_dict(torch.load("path_to_model_weights.pth"))
        return model
    except Exception as e:
        logger.error(f"[AutoencoderLoader] Failed to load autoencoder: {e}", exc_info=True)
        raise
