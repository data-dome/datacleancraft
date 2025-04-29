import pytest
import torch
from datacleancraft.models.autoencoder_loader import load_autoencoder

def test_autoencoder_loading():
    """
    Test that the autoencoder loads correctly and has the expected structure.
    """
    input_dim = 8  # example input size
    model = load_autoencoder(input_dim)

    # Check if model is instance of torch.nn.Module
    assert isinstance(model, torch.nn.Module)

    # Check encoder and decoder existence
    assert hasattr(model, 'encoder')
    assert hasattr(model, 'decoder')

    # Check forward pass shape
    sample_input = torch.randn(2, input_dim)  # batch of 2
    output = model(sample_input)

    assert output.shape == sample_input.shape, "Output shape should match input shape"

def test_autoencoder_invalid_input():
    """
    Test that loading with invalid input raises an exception.
    """
    with pytest.raises(TypeError):
        load_autoencoder("invalid_input")  # Should raise error since input_dim must be int
