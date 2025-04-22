"""
Model conversion utilities for Inferno.
Handles conversion between different model formats (PyTorch, safetensors, JAX/Flax).
"""

import os
import tempfile
from typing import Dict, Any, Optional, Tuple, Union, List
import shutil

from inferno.utils.logger import get_logger

logger = get_logger(__name__)

def is_safetensors_available() -> bool:
    """Check if safetensors is available."""
    try:
        import safetensors
        return True
    except ImportError:
        return False

def is_flax_available() -> bool:
    """Check if Flax is available."""
    try:
        from transformers.utils import is_flax_available
        return is_flax_available()
    except ImportError:
        try:
            import flax # type: ignore[import]
            return True
        except ImportError:
            return False

def is_jax_available() -> bool:
    """Check if JAX is available."""
    try:
        import jax # type: ignore[import]
        return True
    except ImportError:
        return False

def is_torch_available() -> bool:
    """Check if PyTorch is available."""
    try:
        import torch
        return True
    except ImportError:
        return False

def detect_model_format(model_path: str) -> str:
    """
    Detect the format of a model based on its path or directory structure.
    
    Args:
        model_path: Path to the model file or directory
        
    Returns:
        String indicating the model format: 'pytorch', 'safetensors', 'flax', or 'unknown'
    """
    # Check if it's a directory
    if os.path.isdir(model_path):
        # Check for different model files in the directory
        files = os.listdir(model_path)
        
        # Check for safetensors files
        if any(f.endswith('.safetensors') for f in files):
            return 'safetensors'
        
        # Check for PyTorch files
        if any(f.endswith('.bin') for f in files) or any(f == 'pytorch_model.bin' for f in files):
            return 'pytorch'
        
        # Check for Flax files
        if any(f.endswith('.msgpack') for f in files) or any(f == 'flax_model.msgpack' for f in files):
            return 'flax'
            
    # Check if it's a file
    elif os.path.isfile(model_path):
        if model_path.endswith('.safetensors'):
            return 'safetensors'
        elif model_path.endswith('.bin') or model_path.endswith('.pt'):
            return 'pytorch'
        elif model_path.endswith('.msgpack'):
            return 'flax'
    
    # If it's a Hugging Face model ID, we can't determine the format directly
    # We'll assume it's PyTorch as that's the most common
    if '/' in model_path and not os.path.exists(model_path):
        return 'pytorch'  # Default for HF models
        
    return 'unknown'

def convert_pytorch_to_flax(
    model_path: str, 
    model_class: Optional[str] = None,
    dtype: str = "bfloat16",
    output_path: Optional[str] = None
) -> str:
    """
    Convert a PyTorch model to Flax format.
    
    Args:
        model_path: Path to the PyTorch model or Hugging Face model ID
        model_class: Optional model class name (e.g., 'AutoModelForCausalLM')
        dtype: Data type for the converted model ('float32', 'float16', or 'bfloat16')
        output_path: Optional path to save the converted model
        
    Returns:
        Path to the converted model
    """
    if not is_flax_available() or not is_jax_available() or not is_torch_available():
        raise ImportError(
            "Converting PyTorch models to Flax requires flax, jax, and torch to be installed. "
            "Please install them with `pip install flax jax torch`."
        )
    
    try:
        import jax # type: ignore[import]
        import jax.numpy as jnp # type: ignore[import]
        from transformers import AutoConfig
        
        # Determine the model format
        model_format = detect_model_format(model_path)
        logger.info(f"Detected model format: {model_format}")
        
        # Determine the model class if not provided
        if model_class is None:
            try:
                config = AutoConfig.from_pretrained(model_path)
                if hasattr(config, 'architectures') and config.architectures:
                    architecture = config.architectures[0]
                    # Map architecture to model class
                    if "CausalLM" in architecture:
                        model_class = "AutoModelForCausalLM"
                    elif "Seq2SeqLM" in architecture:
                        model_class = "AutoModelForSeq2SeqLM"
                    elif "MaskedLM" in architecture:
                        model_class = "AutoModelForMaskedLM"
                    elif "ConditionalGeneration" in architecture:
                        model_class = "AutoModelForSeq2SeqLM"
                    else:
                        model_class = "AutoModel"
                else:
                    # Default to causal LM as it's most common
                    model_class = "AutoModelForCausalLM"
            except Exception as e:
                logger.warning(f"Could not determine model class from config: {e}")
                model_class = "AutoModelForCausalLM"  # Default
        
        logger.info(f"Using model class: {model_class}")
        
        # Import the appropriate model classes
        if model_class == "AutoModelForCausalLM":
            from transformers import AutoModelForCausalLM, FlaxAutoModelForCausalLM
            pt_class = AutoModelForCausalLM
            flax_class = FlaxAutoModelForCausalLM
        elif model_class == "AutoModelForSeq2SeqLM":
            from transformers import AutoModelForSeq2SeqLM, FlaxAutoModelForSeq2SeqLM
            pt_class = AutoModelForSeq2SeqLM
            flax_class = FlaxAutoModelForSeq2SeqLM
        elif model_class == "AutoModelForMaskedLM":
            from transformers import AutoModelForMaskedLM, FlaxAutoModelForMaskedLM
            pt_class = AutoModelForMaskedLM
            flax_class = FlaxAutoModelForMaskedLM
        else:
            from transformers import AutoModel, FlaxAutoModel
            pt_class = AutoModel
            flax_class = FlaxAutoModel
        
        # Determine JAX dtype
        if dtype == "float32":
            jax_dtype = jnp.float32
        elif dtype == "float16":
            jax_dtype = jnp.float16
        elif dtype == "bfloat16":
            jax_dtype = jnp.bfloat16
        else:
            logger.warning(f"Unknown dtype {dtype}, defaulting to bfloat16")
            jax_dtype = jnp.bfloat16
        
        # Create a temporary directory if no output path is provided
        if output_path is None:
            temp_dir = tempfile.mkdtemp(prefix="inferno_flax_model_")
            output_path = temp_dir
        else:
            os.makedirs(output_path, exist_ok=True)
        
        # Load the PyTorch model
        logger.info(f"Loading PyTorch model from {model_path}")
        pt_model = pt_class.from_pretrained(model_path)
        
        # Convert to Flax
        logger.info(f"Converting model to Flax format with dtype {dtype}")
        flax_model = flax_class.from_pretrained(
            model_path,
            from_pt=True,
            dtype=jax_dtype
        )
        
        # Save the Flax model
        logger.info(f"Saving Flax model to {output_path}")
        flax_model.save_pretrained(output_path)
        
        # Copy the tokenizer and other files if they exist
        if os.path.isdir(model_path):
            for file in os.listdir(model_path):
                if file.startswith('tokenizer') or file == 'vocab.json' or file == 'merges.txt' or file == 'config.json':
                    src_path = os.path.join(model_path, file)
                    dst_path = os.path.join(output_path, file)
                    if os.path.isfile(src_path) and not os.path.exists(dst_path):
                        shutil.copy2(src_path, dst_path)
        
        logger.info(f"Successfully converted PyTorch model to Flax and saved to {output_path}")
        return output_path
        
    except Exception as e:
        logger.error(f"Error converting PyTorch model to Flax: {e}")
        raise

def convert_safetensors_to_flax(
    model_path: str, 
    model_class: Optional[str] = None,
    dtype: str = "bfloat16",
    output_path: Optional[str] = None
) -> str:
    """
    Convert a safetensors model to Flax format.
    
    Args:
        model_path: Path to the safetensors model or Hugging Face model ID
        model_class: Optional model class name (e.g., 'AutoModelForCausalLM')
        dtype: Data type for the converted model ('float32', 'float16', or 'bfloat16')
        output_path: Optional path to save the converted model
        
    Returns:
        Path to the converted model
    """
    if not is_safetensors_available():
        raise ImportError(
            "Converting safetensors models requires safetensors to be installed. "
            "Please install it with `pip install safetensors`."
        )
    
    # The conversion process is similar to PyTorch, as transformers handles safetensors automatically
    return convert_pytorch_to_flax(model_path, model_class, dtype, output_path)

def convert_model_to_flax(
    model_path: str, 
    model_class: Optional[str] = None,
    dtype: str = "bfloat16",
    output_path: Optional[str] = None,
    force_convert: bool = False
) -> str:
    """
    Convert a model to Flax format, automatically detecting the source format.
    
    Args:
        model_path: Path to the model or Hugging Face model ID
        model_class: Optional model class name (e.g., 'AutoModelForCausalLM')
        dtype: Data type for the converted model ('float32', 'float16', or 'bfloat16')
        output_path: Optional path to save the converted model
        force_convert: Whether to force conversion even if the model is already in Flax format
        
    Returns:
        Path to the converted model (either the original path if already Flax, or the new path)
    """
    # Detect the model format
    model_format = detect_model_format(model_path)
    
    # If already Flax and not forcing conversion, return the original path
    if model_format == 'flax' and not force_convert:
        logger.info(f"Model is already in Flax format: {model_path}")
        return model_path
    
    # Convert based on the detected format
    if model_format == 'safetensors':
        logger.info(f"Converting safetensors model to Flax: {model_path}")
        return convert_safetensors_to_flax(model_path, model_class, dtype, output_path)
    else:  # Default to PyTorch for unknown formats
        logger.info(f"Converting PyTorch model to Flax: {model_path}")
        return convert_pytorch_to_flax(model_path, model_class, dtype, output_path)
