#!/usr/bin/env python3
"""
Test script for OpenRouter integration with mLLMCelltype.
This script tests the OpenRouter API with different models.
"""

import os
import sys
import time

# Add the correct path to the mllmcelltype module
package_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, package_dir)

# Import mLLMCelltype functions
from mllmcelltype import annotate_clusters, get_model_response, setup_logging

# Set up logging
setup_logging()

# Set API keys directly for testing
api_keys = {
    "OPENROUTER_API_KEY": "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",
}

# Set environment variables from the API keys
for key, value in api_keys.items():
    os.environ[key] = value

# Define a simple set of marker genes for testing
marker_genes = {
    "0": ["CD3D", "CD3E", "CD3G", "CD2", "CD7", "CD28", "IL7R", "TCF7"],
    "1": ["CD19", "MS4A1", "CD79A", "CD79B", "CD22", "CD20", "PAX5", "CD74"],
    "2": ["CD14", "LYZ", "CSF1R", "CD68", "CD163", "FCGR3A", "FCGR1A", "ITGAM"],
    "3": ["NCAM1", "NKG7", "KLRD1", "KLRF1", "KLRC1", "KLRC2", "FCGR3A", "FCGR3B"],
    "4": ["HBA1", "HBA2", "HBB", "GYPA", "ALAS2", "AHSP", "CA1", "SLC4A1"],
}

def test_openrouter_models():
    """Test OpenRouter with different models."""
    print("Testing OpenRouter integration with different models...")

    # Define OpenRouter models to test
    # Note: Only use models that are actually available on OpenRouter
    openrouter_models = [
        "openai/gpt-4o",
        "anthropic/claude-3-opus",  # Updated to a valid model ID
        "meta-llama/llama-3-70b-instruct",
        "mistralai/mistral-large",
    ]

    results = {}

    # Test each model
    for model in openrouter_models:
        print(f"\n--- Testing OpenRouter with model: {model} ---")
        try:
            start_time = time.time()
            annotations = annotate_clusters(
                marker_genes=marker_genes,
                species="human",
                tissue="blood",
                provider="openrouter",
                model=model,
                use_cache=False,  # Disable cache for testing
            )
            end_time = time.time()

            print(f"✅ Success! Time taken: {end_time - start_time:.2f} seconds")
            print("Annotations:")
            for cluster, cell_type in annotations.items():
                print(f"  Cluster {cluster}: {cell_type}")

            results[model] = {
                "success": True,
                "time": end_time - start_time,
                "annotations": annotations,
            }

            # Add a delay between requests to avoid rate limits
            time.sleep(2)

        except Exception as e:
            print(f"❌ Error with model {model}: {str(e)}")
            results[model] = {
                "success": False,
                "error": str(e),
            }

    # Print summary
    print("\n=== OpenRouter Test Summary ===")
    for model, result in results.items():
        status = "✅ Success" if result["success"] else f"❌ Failed: {result['error']}"
        print(f"{model}: {status}")
        if result["success"]:
            print(f"  Time: {result['time']:.2f} seconds")

    # Return success if at least one model worked
    return any(result["success"] for result in results.values())

def test_simple_query():
    """Test a simple query with OpenRouter."""
    print("\nTesting simple query with OpenRouter...")

    prompt = "What are the marker genes for T cells?"

    try:
        response = get_model_response(
            prompt=prompt,
            provider="openrouter",
            model="openai/gpt-4o",
            use_cache=False
        )

        print("\n--- OpenRouter Response (openai/gpt-4o) ---")
        print(response)
        print("----------------------------------------\n")
        return True
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("=== OpenRouter Integration Test ===")

    # Test simple query
    simple_query_success = test_simple_query()

    # Test multiple models
    models_success = test_openrouter_models()

    # Overall success
    if simple_query_success and models_success:
        print("\n✅ All OpenRouter tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some OpenRouter tests failed!")
        sys.exit(1)
