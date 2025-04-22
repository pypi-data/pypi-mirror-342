#!/usr/bin/env python
"""
Command-line utility to convert models between different formats.
Supports conversion from PyTorch/safetensors to JAX/Flax.
"""

import argparse
import os
import sys
import logging

# Add parent directory to path to allow importing from inferno
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from inferno.models.converter import (
    convert_model_to_flax,
    detect_model_format,
    is_jax_available,
    is_flax_available,
    is_torch_available,
    is_safetensors_available
)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("inferno.tools.convert_model")

def check_dependencies():
    """Check if all required dependencies are installed."""
    missing_deps = []
    
    if not is_torch_available():
        missing_deps.append("torch")
    
    if not is_jax_available():
        missing_deps.append("jax")
    
    if not is_flax_available():
        missing_deps.append("flax")
    
    if not is_safetensors_available():
        missing_deps.append("safetensors")
    
    if missing_deps:
        logger.error(f"Missing dependencies: {', '.join(missing_deps)}")
        logger.error("Please install them with: pip install " + " ".join(missing_deps))
        return False
    
    return True

def main():
    """Main entry point for the model conversion utility."""
    parser = argparse.ArgumentParser(description="Convert models between different formats")
    
    parser.add_argument(
        "--model_path",
        type=str,
        required=True,
        help="Path to the model or Hugging Face model ID"
    )
    
    parser.add_argument(
        "--output_path",
        type=str,
        default=None,
        help="Path to save the converted model (default: creates a directory based on the model name)"
    )
    
    parser.add_argument(
        "--model_class",
        type=str,
        default=None,
        choices=["AutoModelForCausalLM", "AutoModelForSeq2SeqLM", "AutoModelForMaskedLM", "AutoModel"],
        help="Model class to use for conversion (default: auto-detect)"
    )
    
    parser.add_argument(
        "--dtype",
        type=str,
        default="bfloat16",
        choices=["float32", "float16", "bfloat16"],
        help="Data type for the converted model (default: bfloat16)"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    # Set log level
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Detect model format
    model_format = detect_model_format(args.model_path)
    logger.info(f"Detected model format: {model_format}")
    
    # Create output path if not provided
    if args.output_path is None:
        if os.path.isdir(args.model_path):
            model_name = os.path.basename(os.path.normpath(args.model_path))
        elif '/' in args.model_path and not os.path.exists(args.model_path):
            # Hugging Face model ID
            model_name = args.model_path.split('/')[-1]
        else:
            model_name = os.path.basename(args.model_path)
            if model_name.endswith('.bin') or model_name.endswith('.safetensors'):
                model_name = model_name.rsplit('.', 1)[0]
        
        args.output_path = f"{model_name}_flax"
        logger.info(f"No output path provided, using: {args.output_path}")
    
    # Convert the model
    try:
        output_path = convert_model_to_flax(
            model_path=args.model_path,
            model_class=args.model_class,
            dtype=args.dtype,
            output_path=args.output_path
        )
        
        logger.info(f"Model successfully converted and saved to: {output_path}")
        logger.info("You can now use this model with JAX/Flax on TPUs")
        
    except Exception as e:
        logger.error(f"Error converting model: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
