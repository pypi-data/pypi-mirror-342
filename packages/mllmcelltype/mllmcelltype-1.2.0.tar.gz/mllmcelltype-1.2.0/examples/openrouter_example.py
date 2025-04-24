#!/usr/bin/env python3
"""
OpenRouter Integration Example for mLLMCelltype

This example demonstrates how to use OpenRouter with mLLMCelltype to access
multiple LLM providers through a single API.

OpenRouter (https://openrouter.ai) provides a unified API for accessing models from:
- OpenAI (GPT-4o, etc.)
- Anthropic (Claude models)
- Meta (Llama models)
- Mistral AI
- And many more

To use this example:
1. Get an API key from https://openrouter.ai/keys
2. Set the OPENROUTER_API_KEY environment variable or replace the placeholder below
"""

import os
import sys
import pandas as pd
from typing import Dict, List, Optional

# Add the parent directory to the path so we can import mllmcelltype
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import mLLMCelltype functions
from mllmcelltype import (
    annotate_clusters,
    interactive_consensus_annotation,
    print_consensus_summary,
    setup_logging,
)

# Set up logging
setup_logging()

# Set your OpenRouter API key
# You can get one from https://openrouter.ai/keys
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "your-openrouter-api-key")
os.environ["OPENROUTER_API_KEY"] = OPENROUTER_API_KEY

# Example marker genes for different cell types
EXAMPLE_MARKER_GENES = {
    "0": ["CD3D", "CD3E", "CD3G", "CD2", "CD7", "CD28", "IL7R", "TCF7"],  # T cells
    "1": ["CD19", "MS4A1", "CD79A", "CD79B", "CD22", "CD20", "PAX5", "CD74"],  # B cells
    "2": ["CD14", "LYZ", "CSF1R", "CD68", "CD163", "FCGR3A", "FCGR1A", "ITGAM"],  # Monocytes
    "3": ["NCAM1", "NKG7", "KLRD1", "KLRF1", "KLRC1", "KLRC2", "FCGR3A", "FCGR3B"],  # NK cells
    "4": ["HBA1", "HBA2", "HBB", "GYPA", "ALAS2", "AHSP", "CA1", "SLC4A1"],  # Erythrocytes
}

def single_model_annotation(
    marker_genes: Dict[str, List[str]],
    provider: str = "openrouter",
    model: str = "openai/gpt-4o",
    species: str = "human",
    tissue: str = "blood",
) -> Dict[str, str]:
    """
    Annotate cell clusters using a single model via OpenRouter.
    
    Args:
        marker_genes: Dictionary mapping cluster IDs to lists of marker genes
        provider: Provider name (should be 'openrouter')
        model: Model name in 'provider/model-name' format
        species: Species name (e.g., 'human', 'mouse')
        tissue: Tissue name (e.g., 'blood', 'brain')
        
    Returns:
        Dictionary mapping cluster IDs to cell type annotations
    """
    print(f"\nAnnotating clusters using {model} via OpenRouter...")
    
    annotations = annotate_clusters(
        marker_genes=marker_genes,
        species=species,
        tissue=tissue,
        provider=provider,
        model=model,
    )
    
    print(f"Annotations from {model}:")
    for cluster, cell_type in annotations.items():
        print(f"  Cluster {cluster}: {cell_type}")
    
    return annotations

def compare_multiple_models(
    marker_genes: Dict[str, List[str]],
    models: List[str] = ["openai/gpt-4o", "anthropic/claude-3-opus", "meta-llama/llama-3-70b-instruct"],
    species: str = "human",
    tissue: str = "blood",
) -> Dict[str, Dict[str, str]]:
    """
    Compare annotations from multiple models via OpenRouter.
    
    Args:
        marker_genes: Dictionary mapping cluster IDs to lists of marker genes
        models: List of model names in 'provider/model-name' format
        species: Species name (e.g., 'human', 'mouse')
        tissue: Tissue name (e.g., 'blood', 'brain')
        
    Returns:
        Dictionary mapping model names to annotation dictionaries
    """
    print("\nComparing annotations from multiple models via OpenRouter...")
    
    results = {}
    
    for model in models:
        print(f"\nProcessing model: {model}")
        try:
            annotations = annotate_clusters(
                marker_genes=marker_genes,
                species=species,
                tissue=tissue,
                provider="openrouter",
                model=model,
            )
            
            results[model] = annotations
            
            print(f"Annotations from {model}:")
            for cluster, cell_type in annotations.items():
                print(f"  Cluster {cluster}: {cell_type}")
                
        except Exception as e:
            print(f"Error with model {model}: {str(e)}")
            results[model] = {"error": str(e)}
    
    return results

def consensus_annotation(
    marker_genes: Dict[str, List[str]],
    models: List[Dict[str, str]] = None,
    species: str = "human",
    tissue: str = "blood",
) -> Dict:
    """
    Perform consensus annotation using multiple models via OpenRouter.
    
    Args:
        marker_genes: Dictionary mapping cluster IDs to lists of marker genes
        models: List of model configurations
        species: Species name (e.g., 'human', 'mouse')
        tissue: Tissue name (e.g., 'blood', 'brain')
        
    Returns:
        Dictionary with consensus results
    """
    if models is None:
        models = [
            {"provider": "openrouter", "model": "openai/gpt-4o"},
            {"provider": "openrouter", "model": "anthropic/claude-3-opus"},
            {"provider": "openrouter", "model": "meta-llama/llama-3-70b-instruct"},
            {"provider": "openrouter", "model": "mistralai/mistral-large"},
        ]
    
    print("\nPerforming consensus annotation with multiple models via OpenRouter...")
    
    # Print model configuration
    print("Model configuration:")
    for model_config in models:
        print(f"  - Provider: {model_config['provider']}, Model: {model_config['model']}")
    
    # Run consensus annotation
    result = interactive_consensus_annotation(
        marker_genes=marker_genes,
        species=species,
        tissue=tissue,
        models=models,
        consensus_threshold=0.7,
        max_discussion_rounds=2,
        verbose=True,
    )
    
    # Print consensus summary
    print("\nConsensus annotation results:")
    print_consensus_summary(result)
    
    return result

def main():
    """Main function to demonstrate OpenRouter integration."""
    print("=" * 80)
    print("OpenRouter Integration Example for mLLMCelltype")
    print("=" * 80)
    
    # Check if API key is set
    if OPENROUTER_API_KEY == "your-openrouter-api-key":
        print("Please set your OpenRouter API key in the script or as an environment variable.")
        print("You can get an API key from https://openrouter.ai/keys")
        sys.exit(1)
    
    # 1. Single model annotation
    single_model_annotation(
        marker_genes=EXAMPLE_MARKER_GENES,
        provider="openrouter",
        model="openai/gpt-4o",
    )
    
    # 2. Compare multiple models
    compare_multiple_models(
        marker_genes=EXAMPLE_MARKER_GENES,
        models=["openai/gpt-4o", "anthropic/claude-3-opus", "meta-llama/llama-3-70b-instruct"],
    )
    
    # 3. Consensus annotation
    consensus_annotation(
        marker_genes=EXAMPLE_MARKER_GENES,
        models=[
            {"provider": "openrouter", "model": "openai/gpt-4o"},
            {"provider": "openrouter", "model": "anthropic/claude-3-opus"},
            {"provider": "openrouter", "model": "meta-llama/llama-3-70b-instruct"},
            {"provider": "openrouter", "model": "mistralai/mistral-large"},
        ],
    )
    
    print("\nOpenRouter integration example completed successfully!")

if __name__ == "__main__":
    main()
