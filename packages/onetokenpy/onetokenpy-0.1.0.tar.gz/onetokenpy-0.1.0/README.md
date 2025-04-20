# onetokenpy

A Python library for running local LLM classification tasks on data. Supports both GPU (using vLLM) and CPU (using llama.cpp) inference.

## Installation

### Basic Installation (CPU only)
Installs the package with CPU support using `llama-cpp-python`.
```bash
pip install onetokenpy
```

### GPU Support
If you have a CUDA-compatible GPU and want to use vLLM for faster inference:
```bash
pip install "onetokenpy[gpu]"
```

## Usage

```python
import onetokenpy as ot
import pandas as pd

# Create a sample dataframe
df = pd.DataFrame({
    'postal_codes': ['H2X 1Y1', '12345', 'ABC123', 'K1A 0B1']
})

# Classify the postal codes using the default CPU model
# (google/gemma-3-1b-it-qat-q4_0-gguf)
result = ot.classify(
    df,
    "Classify this {postal_codes} as whether it is a correctly formatted Canadian postal code. Answer only by Yes or No"
)

print(result)
```

## Features

- Run local LLM classification tasks on pandas DataFrames or lists of strings.
- Automatic backend selection (GPU if available and `[gpu]` extra installed, otherwise CPU).
- Uses vLLM for GPU inference (requires `pip install "onetokenpy[gpu]"`).
- Uses llama.cpp via `llama-cpp-python` for CPU inference.
- Downloads required models (GGUF for llama.cpp, standard HF format for vLLM) automatically via `huggingface_hub`.
- Returns results as a pandas DataFrame including original data, classifications, and generated prompts.

## Requirements

- Python 3.8+
- `pandas`
- `llama-cpp-python` (for CPU support, installed by default)
- `huggingface-hub` (for model downloading, installed by default)
- For GPU support: 
    - CUDA-compatible GPU
    - `vllm` (install via `pip install "onetokenpy[gpu]"`)

## License

MIT License

## Author

Maxime Rivest (mrive052@gmail.com) 