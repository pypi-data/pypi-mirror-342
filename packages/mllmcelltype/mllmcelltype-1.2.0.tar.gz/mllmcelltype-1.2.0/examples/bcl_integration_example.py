#!/usr/bin/env python3
"""
Test script for mLLMCelltype with Scanpy integration.
Uses API keys from .env file in the mLLMCelltype directory.
"""

import os
import sys

# Set matplotlib to non-interactive mode to avoid plotting blocks
import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")  # Use Agg backend, which is a non-interactive backend
import matplotlib.pyplot as plt
import scanpy as sc

# Turn off interactive plotting
plt.ioff()

import shutil

from dotenv import load_dotenv

# Add the correct path to the mllmcelltype module
package_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, package_dir)

# Import mLLMCelltype functions
from mllmcelltype import (
    annotate_clusters,
    interactive_consensus_annotation,
    setup_logging,
)

# Load API keys from .env file
# Try to find .env file in various locations
env_path = None

# Try current directory
if os.path.exists(".env"):
    env_path = ".env"

# Try parent directories
if not env_path:
    current_dir = os.path.abspath(os.getcwd())
    for _ in range(3):  # Check up to 3 parent directories
        parent_dir = os.path.dirname(current_dir)
        potential_path = os.path.join(parent_dir, ".env")
        if os.path.exists(potential_path):
            env_path = potential_path
            break
        if parent_dir == current_dir:  # Reached root directory
            break
        current_dir = parent_dir

# Try package directory
if not env_path:
    package_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    potential_path = os.path.join(package_dir, ".env")
    if os.path.exists(potential_path):
        env_path = potential_path

if env_path:
    load_dotenv(env_path)
    print(f"Loaded environment variables from {env_path}")
else:
    print("No .env file found. Please set API keys as environment variables.")

# Set up logging
setup_logging()

# Load BCL dataset from specified path
print("Loading BCL dataset...")

# Try different possible paths for the BCL dataset
possible_paths = [
    "/Users/apple/Research/LLMCelltype/data/raw/BCL.h5ad",  # Original path
    "../data/raw/BCL.h5ad",  # Relative to examples directory
    "data/raw/BCL.h5ad",  # Relative to project root
    "/Users/apple/Research/mLLMCelltype/data/raw/BCL.h5ad",  # Updated path with mLLMCelltype
]

bcl_data_path = None
for path in possible_paths:
    if os.path.exists(path):
        bcl_data_path = path
        print(f"Found BCL dataset at: {path}")
        break

if not bcl_data_path:
    print("BCL dataset not found. Please provide the correct path.")
    # Create a small dummy dataset for testing
    print("Creating a small dummy dataset for testing...")
    adata = sc.datasets.pbmc3k()
    print("Using PBMC dataset as a substitute")
else:
    adata = sc.read_h5ad(bcl_data_path)
print(f"Loaded dataset with {adata.shape[0]} cells and {adata.shape[1]} genes")

# Preprocess the data
print("Preprocessing data...")
sc.pp.filter_cells(adata, min_genes=200)
sc.pp.filter_genes(adata, min_cells=3)
sc.pp.normalize_total(adata, target_sum=1e4)
sc.pp.log1p(adata)
sc.pp.highly_variable_genes(adata, min_mean=0.0125, max_mean=3, min_disp=0.5)
adata = adata[:, adata.var.highly_variable]
sc.pp.scale(adata, max_value=10)
sc.tl.pca(adata, svd_solver="arpack")
sc.pp.neighbors(adata, n_neighbors=10, n_pcs=40)
sc.tl.umap(adata)
sc.tl.leiden(adata, resolution= 0.061)
print(f"Identified {len(adata.obs['leiden'].cat.categories)} clusters")

# Run differential expression analysis to get marker genes
print("Finding marker genes...")
sc.tl.rank_genes_groups(adata, "leiden", method="wilcoxon")

# Extract marker genes for each cluster
marker_genes = {}
for i in range(len(adata.obs["leiden"].cat.categories)):
    # Extract top 10 genes for each cluster
    genes = [adata.uns["rank_genes_groups"]["names"][str(i)][j] for j in range(10)]
    marker_genes[str(i)] = genes
    print(f"Cluster {i} markers: {', '.join(genes[:3])}...")

# Set API keys directly for testing
api_keys = {
    "OPENAI_API_KEY": "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",
    "ANTHROPIC_API_KEY": "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",
    "DEEPSEEK_API_KEY": "sk-b9d954f8449949168dcab3b21ed1dd22",
    "GEMINI_API_KEY": "AIzaSyDqD_trJuYDSIYO1TWHlOCveV9qQXUJ6uE",
    "QWEN_API_KEY": "sk-4d1266fd8cac4ef7a36efe0c628d68a6",
    "ZHIPU_API_KEY": "050850e5408a4e18baa821662d26f970.TThHkWZx5DpwKah5",
    "STEPFUN_API_KEY": "4H8ESjSb1Jgbl445kNARZyro4AWVzc9JX2RXX8ljZOR23HHyAu3MqN2NiD7P5STTp",
    "MINIMAX_API_KEY": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJHcm91cE5hbWUiOiJDYWZmZXJ5IFlhbmciLCJVc2VyTmFtZSI6IkNhZmZlcnkgWWFuZyIsIkFjY291bnQiOiIiLCJTdWJqZWN0SUQiOiIxODkwOTcxNzE4MzY5OTM5NjU4IiwiUGhvbmUiOiIiLCJHcm91cElEIjoiMTg5MDk3MTcxODM2NTc0NTM1NCIsIlBhZ2VOYW1lIjoiIiwiTWFpbCI6ImNhZmZlcnljaGVuNzg1MEBnbWFpbC5jb20iLCJDcmVhdGVUaW1lIjoiMjAyNS0wMi0xNiAxODoxNTozMiIsIlRva2VuVHlwZSI6MSwiaXNzIjoibWluaW1heCJ9.FE72wZF1DAzhTRjEh4D8lcUcJwQsmBMQf5umCTLV_UBckTAVoguyC7k-8_ddbcptfY6OFG-V0QxzF9kmNLMKX-Grm8NqdrBvjUsX2Ngn8NwQmGzBTi21x1DfXrIOcCknu6uwmbdSF9GvOfHlx_CL__JC52ESVW6cqV0Y1LMcA_i4PQbIy_yOVl1Ha39iEhR9cWsztHQTPZjhGlolXC1X3vCh3r4vCOBdVIk7tA-vqy0fblobnn-5VWoI3mVeIfyMCUbgIWPs4WmCY7DR3a-bvkn27IzlMJfZlT8ySsWrT_eRoAsBCFO16lu9bmNu2fud9BS0Le6mLdc2BcuOMp__Zg",
    "GROK_API_KEY": "xai-k62wSFe3dN9Fp19ShiQI784ZGuARIMfNgBN5lQg8r4GTkGh3Qc89baLTYRpmrenM4puyJzj3c4Gkzlhz",
    "OPENROUTER_API_KEY": "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",
    "MINIMAX_GROUP_ID": "1890971718365745354",
}

# Set environment variables from the API keys
for key, value in api_keys.items():
    os.environ[key] = value

available_apis = [k for k, v in api_keys.items() if v]
print(f"Available API keys: {', '.join(available_apis)}")

if not available_apis:
    print("No API keys found in .env file. Please add your API keys.")
    sys.exit(1)

# Determine which models to use based on available API keys
models = []
if os.getenv("OPENAI_API_KEY"):
    models.append("gpt-4o")
if os.getenv("ANTHROPIC_API_KEY"):
    models.append("claude-3-5-sonnet-latest")
if os.getenv("GEMINI_API_KEY"):
    models.append("gemini-1.5-pro")
if os.getenv("QWEN_API_KEY"):
    models.append("qwen-max")
if os.getenv("OPENROUTER_API_KEY"):
    # Add multiple OpenRouter models to showcase its capabilities
    # Format: (provider, model_id)
    # For OpenRouter, the model_id must include the provider prefix
    models.append({"provider": "openrouter", "model": "openai/gpt-4o"})  # OpenAI via OpenRouter
    models.append({"provider": "openrouter", "model": "anthropic/claude-3-opus"})  # Anthropic via OpenRouter
    models.append({"provider": "openrouter", "model": "meta-llama/llama-3-70b-instruct"})  # Meta Llama via OpenRouter
    models.append({"provider": "openrouter", "model": "mistralai/mistral-large"})  # Mistral AI via OpenRouter
    # Note: Some models like google/gemini-1.5-pro are not available on OpenRouter

# Format model list for printing
model_names = []
for model in models:
    if isinstance(model, dict):
        if model.get('provider') == 'openrouter':
            model_names.append(f"openrouter/{model.get('model')}")
        else:
            model_names.append(f"{model.get('provider')}/{model.get('model')}")
    elif isinstance(model, tuple):
        model_names.append(f"{model[0]}/{model[1]}")
    else:
        model_names.append(model)

print(f"Using models: {', '.join(model_names)}")

if len(models) < 2:
    print("Warning: For consensus annotation, at least 2 models are recommended.")
    # Fall back to single model annotation if only one API key is available
    if len(models) == 1:
        print(f"Performing single model annotation with {models[0]}...")
        # Handle both string models and tuple models (provider, model)
        if isinstance(models[0], tuple):
            provider, model = models[0]
        else:
            model = models[0]
            provider = (
                "openai"
                if "gpt" in model
                else (
                    "anthropic"
                    if "claude" in model
                    else "gemini" if "gemini" in model else "qwen"
                )
            )

        print(f"Using provider: {provider}, model: {model}")
        annotations = annotate_clusters(
            marker_genes=marker_genes,
            species="human",
            tissue="blood",
            provider=provider,
            model=model,
        )

        # Add annotations to AnnData object
        adata.obs["cell_type"] = adata.obs["leiden"].astype(str).map(annotations)

        # Visualize results
        sc.pl.umap(
            adata,
            color="cell_type",
            legend_loc="on data",
            save="_single_model_annotation.png",
        )
        print(f"Results saved as figures/umap_single_model_annotation.png")

        # Print annotations
        print("\nCluster annotations:")
        for cluster, annotation in annotations.items():
            print(f"Cluster {cluster}: {annotation}")

        sys.exit(0)
    else:
        print("No models available. Please add API keys to .env file.")
        sys.exit(1)

# Run consensus annotation with multiple models
print("\nRunning consensus annotation with multiple models...")

# Prepare models and providers for consensus annotation
model_config = []
for model_item in models:
    if isinstance(model_item, dict):
        # 如果已经是字典格式，直接添加
        model_config.append(model_item)
    elif isinstance(model_item, tuple):
        provider, model = model_item
        model_config.append({"provider": provider, "model": model})
    else:
        model = model_item
        if "gpt" in model:
            provider = "openai"
        elif "claude" in model:
            provider = "anthropic"
        elif "gemini" in model:
            provider = "gemini"
        elif "qwen" in model:
            provider = "qwen"
        else:
            provider = "unknown"
        model_config.append({"provider": provider, "model": model})

print("Model configuration for consensus annotation:")
for cfg in model_config:
    print(f"  - Provider: {cfg['provider']}, Model: {cfg['model']}")

consensus_results = interactive_consensus_annotation(
    marker_genes=marker_genes,
    species="human",
    tissue="blood",
    models=model_config,
    consensus_threshold=0.7,  # Adjust threshold for consensus agreement
    max_discussion_rounds=3,  # Maximum rounds of discussion between models
    verbose=True,
)

# Access the final consensus annotations from the dictionary
final_annotations = consensus_results["consensus"]

# Add consensus annotations to AnnData object
adata.obs["consensus_cell_type"] = (
    adata.obs["leiden"].astype(str).map(final_annotations)
)

# Add consensus proportion and entropy metrics to AnnData object
adata.obs["consensus_proportion"] = (
    adata.obs["leiden"].astype(str).map(consensus_results["consensus_proportion"])
)
adata.obs["entropy"] = adata.obs["leiden"].astype(str).map(consensus_results["entropy"])

# Visualize results
plt.figure(figsize=(12, 10))
sc.pl.umap(
    adata,
    color="consensus_cell_type",
    legend_loc="on data",
    save="_consensus_annotation.png",
)
sc.pl.umap(adata, color="consensus_proportion", save="_consensus_proportion.png")
sc.pl.umap(adata, color="entropy", save="_entropy.png")

print("\nResults saved as:")
print("- figures/umap_consensus_annotation.png")
print("- figures/umap_consensus_proportion.png")
print("- figures/umap_entropy.png")

# Print consensus annotations with uncertainty metrics
print("\nConsensus annotations with uncertainty metrics:")
for cluster in sorted(final_annotations.keys(), key=int):
    cp = consensus_results["consensus_proportion"][cluster]
    entropy = consensus_results["entropy"][cluster]
    print(
        f"Cluster {cluster}: {final_annotations[cluster]} (CP: {cp:.2f}, Entropy: {entropy:.2f})"
    )

# Save results
result_file = "consensus_results.txt"
with open(result_file, "w") as f:
    f.write("Cluster\tCell Type\tConsensus Proportion\tEntropy\n")
    for cluster in sorted(final_annotations.keys(), key=int):
        cp = consensus_results["consensus_proportion"][cluster]
        entropy = consensus_results["entropy"][cluster]
        f.write(f"{cluster}\t{final_annotations[cluster]}\t{cp:.2f}\t{entropy:.2f}\n")

print(f"\nDetailed results saved to {result_file}")
print("\nTest completed successfully!")
