import pytest
import pandas as pd
import numpy as np
from datacleancraft.validation.anomaly_detector import AnomalyDetector

def test_detect_anomalies_output_structure(sample_data):
    """Test if detect_anomalies returns expected structure."""
    detector = AnomalyDetector(threshold=0.1)
    result = detector.detect_anomalies(sample_data)

    # Check columns
    assert "anomaly_score" in result.columns
    assert "is_anomaly" in result.columns

    # Check types
    assert pd.api.types.is_float_dtype(result["anomaly_score"])
    assert pd.api.types.is_bool_dtype(result["is_anomaly"])

def test_detect_anomalies_flagging(sample_data):
    """Test if anomalies are correctly flagged."""
    detector = AnomalyDetector(threshold=0.1)
    result = detector.detect_anomalies(sample_data)

    # There should be at least one anomaly detected
    assert result["is_anomaly"].sum() >= 1

def test_empty_numeric_dataframe():
    """Test handling when no numeric columns exist."""
    df = pd.DataFrame({
        "text1": ["a", "b", "c"],
        "text2": ["x", "y", "z"]
    })

    detector = AnomalyDetector(threshold=0.5)

    #with pytest.raises(ValueError, match="No numeric data available for anomaly detection."):
    assert detector.detect_anomalies(df) == None

def test_all_anomalies_detection():
    """Test edge case when all rows are anomalies."""
    extreme_data = pd.DataFrame({
        "feature1": [1000, 2000, 3000],
        "feature2": [1500, 2500, 3500]
    })

    detector = AnomalyDetector(threshold=0.01)
    result = detector.detect_anomalies(extreme_data)

    assert result["is_anomaly"].all()

def test_no_anomalies_detection():
    """Test edge case when no rows are anomalies."""
    normal_data = pd.DataFrame({
        "feature1": [0.1, 0.2, 0.3],
        "feature2": [0.1, 0.2, 0.3]
    })

    detector = AnomalyDetector(threshold=10.0)
    result = detector.detect_anomalies(normal_data)

    assert not result["is_anomaly"].any()
