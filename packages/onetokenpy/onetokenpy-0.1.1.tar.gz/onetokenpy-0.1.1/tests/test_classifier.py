import pytest
import pandas as pd
from onetokenpy.classifier import classify

def test_classify_with_dataframe(sample_dataframe, prompt_template):
    # Run classification
    result = classify(sample_dataframe, prompt_template)
    
    # Verify the result structure
    assert isinstance(result, pd.DataFrame)
    assert 'postal_codes' in result.columns
    assert 'classification' in result.columns
    assert 'prompt' in result.columns
    assert len(result) == 4
    
    # Verify the prompts were correctly formatted
    for prompt in result['prompt']:
        assert 'Classify this' in prompt
        assert 'as whether it is a correctly formatted postal code' in prompt
        assert 'Answer only by Yes or No' in prompt

def test_classify_with_list(sample_postal_codes, prompt_template):
    # Run classification
    result = classify(sample_postal_codes, prompt_template)
    
    # Verify the result structure
    assert isinstance(result, pd.DataFrame)
    assert 'value' in result.columns
    assert 'classification' in result.columns
    assert 'prompt' in result.columns
    assert len(result) == 4
    
    # Verify the prompts were correctly formatted
    for prompt in result['prompt']:
        assert 'Classify this' in prompt
        assert 'as whether it is a correctly formatted postal code' in prompt
        assert 'Answer only by Yes or No' in prompt 