import pandas as pd
import torch
from typing import List, Union, Optional, Dict, Any
from pathlib import Path
import os
import functools # Import functools for lru_cache
from huggingface_hub import hf_hub_download, HfApi
from huggingface_hub.utils import EntryNotFoundError # Import specific error
import string # Import string module for Formatter

# Default max tokens if not specified in classify call
DEFAULT_MAX_TOKENS = 10 # Increased default slightly

class CPUEngine:
    """Engine for CPU-based inference using llama.cpp"""
    def __init__(self, model_path: str):
        try:
            global Llama # Make class available globally if imported
            from llama_cpp import Llama
        except ImportError:
             raise ImportError("llama-cpp-python is not installed. Please install it: pip install llama-cpp-python")

        try:
            resolved_model_path = _resolve_model_path_gguf(model_path)
            print(f"Loading Llama model from: {resolved_model_path}")
            # Consider adding chat_format if auto-detection isn't sufficient for your models
            self.llm = Llama(model_path=resolved_model_path, n_ctx=2048, n_threads=os.cpu_count() or 4, verbose=False)
        except ValueError as e:
            raise ValueError(f"Failed to resolve model path for llama.cpp: {e}")
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Llama model: {e}")

    def classify(self, prompts: List[str], system_prompt: Optional[str] = None, max_tokens: Optional[int] = None) -> List[str]:
        """Classify prompts using llama.cpp's create_chat_completion."""
        resolved_max_tokens = max_tokens if max_tokens is not None else DEFAULT_MAX_TOKENS
        classifications = []

        for user_prompt in prompts:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": user_prompt})

            try:
                # Use create_chat_completion
                completion = self.llm.create_chat_completion(
                    messages=messages,
                    max_tokens=resolved_max_tokens,
                    temperature=0.0
                )
                # Extract content from the response structure
                if (completion and "choices" in completion and 
                    len(completion["choices"]) > 0 and "message" in completion["choices"][0] and
                    "content" in completion["choices"][0]["message"]):
                     response_content = completion["choices"][0]["message"]["content"]
                     classifications.append(response_content.strip() if response_content else "")
                else:
                     print(f"Warning: Unexpected chat completion format from llama.cpp for prompt: {user_prompt[:50]}...")
                     classifications.append("")
            except Exception as e:
                print(f"Warning: Error during llama.cpp chat completion for prompt: {user_prompt[:50]}... Error: {e}")
                classifications.append("")
        return classifications

class GPUEngine:
    """Engine for GPU-based inference using vLLM"""
    def __init__(self, model_path: str):
        try:
            global LLM, SamplingParams # Make classes available globally
            from vllm import LLM, SamplingParams
        except ImportError:
             raise ImportError("vLLM is not installed. Please install it for GPU support: pip install 'onetokenpy[gpu]'")

        try:
            print(f"Loading vLLM model: {model_path}")
            self.model_path = model_path
            self.llm = LLM(model=model_path)
            # Store default max_tokens, but SamplingParams are now created per-call in classify
            self.default_max_tokens = DEFAULT_MAX_TOKENS
        except Exception as e:
            raise RuntimeError(f"Failed to initialize vLLM engine: {e}")

    # Removed _get_vllm_tokenizer and manual chat template logic

    def classify(self, prompts: List[str], system_prompt: Optional[str] = None, max_tokens: Optional[int] = None) -> List[str]:
        """Classify prompts using vLLM's chat method."""
        resolved_max_tokens = max_tokens if max_tokens is not None else self.default_max_tokens
        # Create SamplingParams for this specific call
        current_sampling_params = SamplingParams(temperature=0.0, max_tokens=resolved_max_tokens)

        all_messages = [] # List of conversations
        for user_prompt in prompts:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": user_prompt})
            all_messages.append(messages)

        try:
            # Use the llm.chat() method
            print(f"Calling vLLM chat endpoint with {len(all_messages)} conversations...")
            outputs = self.llm.chat(messages=all_messages, sampling_params=current_sampling_params)
            
            results = []
            for output in outputs:
                 # Extract response from the output object
                 if output.outputs and output.outputs[0].message:
                     response_content = output.outputs[0].message.content
                     results.append(response_content.strip() if response_content else "")
                 else:
                      print(f"Warning: Unexpected output structure in vLLM chat response for request {output.request_id}")
                      results.append("") 
            return results
        except Exception as e:
            print(f"Warning: Error during vLLM chat inference: {e}")
            # Return empty strings for all prompts in case of batch failure
            return [""] * len(prompts)


# --- Cached Engine Getter ---
@functools.lru_cache(maxsize=None) # Cache engine instances indefinitely
def _get_cached_engine(model_path: str, backend: str):
    """Creates and caches engine instances based on model_path and backend."""
    print(f"Attempting to get or create engine for model='{model_path}', backend='{backend}'")
    # NOTE: Engine initialization requires importing the respective libraries.
    # If these libraries are large, this function might be slow on first call for a backend.
    if backend == "cuda":
        try:
            return GPUEngine(model_path)
        except (ImportError, ValueError, RuntimeError) as e:
             raise RuntimeError(f"Failed to initialize GPUEngine: {e}")
    elif backend == "cpu":
        try:
            return CPUEngine(model_path)
        except (ImportError, ValueError, RuntimeError) as e:
             raise RuntimeError(f"Failed to initialize CPUEngine: {e}")
    else:
        raise ValueError(f"Invalid backend specified for engine creation: {backend}")

# --- Helper Functions ---
# _resolve_model_path_gguf remains the same
# ... existing _resolve_model_path_gguf code ...
def _resolve_model_path_gguf(model_path: str) -> str:
    """
    Resolve the model path for GGUF models, downloading from Hugging Face if necessary.
    Checks for local path first, then tries to download from HF hub.
    """
    if os.path.exists(model_path):
        print(f"Using local model file: {model_path}")
        return model_path

    if "/" not in model_path:
         raise ValueError(f"Invalid model path: '{model_path}'. Path does not exist locally and is not a valid Hugging Face repo ID (e.g., 'google/gemma-2b').")

    print(f"'{model_path}' not found locally. Attempting to download GGUF from Hugging Face Hub...")
    try:
        api = HfApi()
        repo_files = api.list_repo_files(repo_id=model_path)
        gguf_files = [f for f in repo_files if f.lower().endswith(".gguf")]

        if not gguf_files:
             print(f"No .gguf files listed in root of {model_path}. Trying to download '{model_path}' directly as a file...")
             try:
                 parts = model_path.split('/')
                 repo_id_part = "/".join(parts[:-1])
                 filename_part = parts[-1]
                 if len(parts) > 1 and filename_part.lower().endswith(".gguf"):
                     local_path = hf_hub_download(repo_id=repo_id_part, filename=filename_part)
                     print(f"Successfully downloaded specific file: {filename_part}")
                     return local_path
                 else:
                     raise EntryNotFoundError("Path does not point to a specific .gguf file.")
             except EntryNotFoundError:
                  raise ValueError(f"No GGUF files found in repository '{model_path}' and path doesn't point to a specific GGUF file.")

        target_filename = gguf_files[0]
        print(f"Found GGUF file: '{target_filename}'. Downloading...")
        local_path = hf_hub_download(
            repo_id=model_path,
            filename=target_filename
        )
        print(f"Model downloaded to: {local_path}")
        return local_path

    except EntryNotFoundError:
         raise ValueError(f"Hugging Face repository or file not found: '{model_path}'")
    except Exception as e:
        raise ValueError(f"Failed to download GGUF model from '{model_path}': {str(e)}")

# _process_prompts remains the same
# ... existing _process_prompts code ...
def _process_prompts(data: Union[pd.DataFrame, List[str]], prompt_template: str) -> List[str]:
    """Process input data into prompts using the template."""
    try:
        if isinstance(data, pd.DataFrame):
            formatter = string.Formatter()
            template_vars = {field_name for _, field_name, _, _ in formatter.parse(prompt_template) if field_name is not None}
            missing_cols = template_vars - set(data.columns)
            if missing_cols:
                 raise ValueError(f"Missing columns in DataFrame required by prompt_template: {missing_cols}")
            return [prompt_template.format(**row) for row in data.to_dict('records')]
        elif isinstance(data, list) and all(isinstance(item, str) for item in data):
            formatter = string.Formatter()
            template_vars = {field_name for _, field_name, _, _ in formatter.parse(prompt_template) if field_name is not None}
            if not template_vars:
                print("Warning: Prompt template has no placeholders. Applying template directly to each list item.")
                return [prompt_template] * len(data)
            elif template_vars != {'text'}:
                 raise ValueError(f"Prompt template for list input must contain only the '{{text}}' placeholder, but found: {template_vars}")
            return [prompt_template.format(text=text) for text in data]
        else:
            raise TypeError("Input data must be a pandas DataFrame or a list of strings.")
    except KeyError as e:
        raise ValueError(f"Failed to format prompt. Make sure your prompt_template placeholders match DataFrame columns or use '{{text}}' for list input. Error: Missing key {e}")
    except Exception as e:
        raise RuntimeError(f"Error processing prompts with template '{prompt_template[:50]}...': {e}")

# --- Main Classification Function ---
def classify(
    data: Union[pd.DataFrame, List[str]],
    prompt_template: str,
    model_path: str = "google/gemma-3-1b-it-qat-q4_0-gguf",
    device: Optional[str] = None,
    system_prompt: Optional[str] = None, # Added system_prompt
    max_tokens: Optional[int] = None     # Added max_tokens
) -> pd.DataFrame:
    """Classify the input data using the LLM.

    Args:
        data: Input data as pandas DataFrame or list of strings.
              If DataFrame, column names are used for prompt_template formatting.
              If list of strings, prompt_template must use '{text}'.
        prompt_template: Template string for user prompts (e.g., "Classify: {text}").
        model_path: Path to the model file or Hugging Face model ID.
                    Default is "google/gemma-3-1b-it-qat-q4_0-gguf".
        device: Device to use ('cuda' or 'cpu'). If None, detects automatically.
        system_prompt: Optional system prompt to guide the model's behavior.
        max_tokens: Maximum tokens to generate for each classification.

    Returns:
        DataFrame with original data and classification results
    """
    # Detect device if not specified
    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Auto-detected device: {device}")
    elif device not in ['cuda', 'cpu']:
        raise ValueError(f"Invalid device specified: '{device}'. Must be 'cuda' or 'cpu'.")

    # Process prompts from data
    try:
        processed_prompts = _process_prompts(data, prompt_template)
        print(f"Processed {len(processed_prompts)} prompts")
    except Exception as e:
        raise ValueError(f"Failed to process prompts: {e}")

    # Get engine (cached) and run classification
    try:
        engine = _get_cached_engine(model_path, device)
        classifications = engine.classify(processed_prompts, system_prompt, max_tokens)
    except Exception as e:
        raise RuntimeError(f"Classification failed: {e}")

    # Return results in a DataFrame
    if isinstance(data, pd.DataFrame):
        result_df = data.copy()
        result_df['classification'] = classifications
        result_df['prompt'] = processed_prompts
        return result_df
    else:
        return pd.DataFrame({
            'text': data,
            'classification': classifications,
            'prompt': processed_prompts
        }) 