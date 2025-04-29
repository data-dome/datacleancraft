import pytest
import pandas as pd
from datacleancraft.preprocessing.cleaner import TextCleaner #lean_text, clean_text_dataframe

# Test the clean_text function
def test_clean_text():
    textcleaner = TextCleaner()

    # Test simple case with no stopwords, punctuation, and correct spelling
    input_text = "I am learning NLP"
    expected_output = "learn nap"  # Lemmatized output after stopword removal and spelling correction
    assert textcleaner.clean_text(input_text) == expected_output

    # Test case with punctuation and numbers
    input_text = "Hello, I am learning 2.0 NLP!!!"
    expected_output = "hello learn 20 nlp"  # Punctuation and numbers should be removed
    assert textcleaner.clean_text(input_text) == expected_output

    # Test case with stopwords
    input_text = "This is a test sentence"
    expected_output = "test sentence"  # Stopwords removed, lemmatization applied
    assert textcleaner.clean_text(input_text) == expected_output

    # Test case with spelling error
    input_text = "I am recieveing a payment"
    expected_output = "receive payment"  # Spelling correction applied
    assert textcleaner.clean_text(input_text) == expected_output

    # Test with None input
    assert textcleaner.clean_text(None) is None  # Should return None if the input is None

    # Test with non-string input
    assert textcleaner.clean_text(12345) == 12345  # Should return the input as it is if it's not a string

# Test the clean_text_dataframe function
def test_clean_text_dataframe():
    
    # Create a sample DataFrame for testing
    data = {
        "col1": ["This is a test sentence", "Another test!"],
        "col2": ["I am learning NLP.", "Spelling error receiveing."]
    }
    df = pd.DataFrame(data)
    
    textcleaner = TextCleaner()

    # Apply the clean_text_dataframe function
    cleaned_df = textcleaner.clean_text_dataframe(df)

    # Expected cleaned dataframe
    expected_data = {
        "col1": ["test sentence", "test"],
        "col2": ["learn nap", "spell error receive"]
    }
    expected_df = pd.DataFrame(expected_data)

    print(cleaned_df)
    # Compare the cleaned DataFrame with the expected one
    pd.testing.assert_frame_equal(cleaned_df, expected_df)

# Test for edge cases in cleaning
def test_edge_cases():
    # Test case with an empty string
    textcleaner = TextCleaner()

    assert textcleaner.clean_text("") == ""  # Empty string should remain empty

    # Test case with single character
    assert textcleaner.clean_text("M") == "m"  # Single character should be normalized to lowercase

    # Test case with no punctuation or stopwords
    assert textcleaner.clean_text("AI") == "ai"  # "AI" should be converted to lowercase and remain as is

    # Test case with multiple spaces between words
    input_text = "This    is   a   test   sentence"
    expected_output = "test sentence"  # Extra spaces should be removed
    assert textcleaner.clean_text(input_text) == expected_output

# Test if NLP model is correctly loaded and used (using spaCy)
def test_spacy_model_loading():
    textcleaner = TextCleaner()
    input_text = "I am using spaCy for NLP tasks."
    output_text = textcleaner.clean_text(input_text)
    assert "task" in output_text and "space" in output_text  # Ensure spaCy's lemmatization worked

