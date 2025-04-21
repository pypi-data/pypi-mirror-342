import os
import torch
import pytest
import tempfile
from pathlib import Path

from embzip.core import quantize, save, load

@pytest.fixture
def sample_embeddings():
    # Create sample embeddings: 100 vectors with 768 dimensions
    return torch.randn(100, 768)


def test_quantize_basic(sample_embeddings):
    """Test basic quantization functionality"""
    quantized = quantize(sample_embeddings)
    
    # Check shapes match
    assert quantized.shape == sample_embeddings.shape
    
    # Check embeddings are different but similar
    assert not torch.allclose(quantized, sample_embeddings)
    
    # Check cosine similarity is reasonably high (not perfect, but not random)
    cos_sim = torch.nn.functional.cosine_similarity(
        sample_embeddings.view(-1), quantized.view(-1), dim=0
    )
    assert 0.5 < cos_sim < 1.0, f"Cosine similarity {cos_sim} out of expected range"


def test_quantize_custom_m(sample_embeddings):
    """Test quantization with custom M parameter"""
    # Default M
    default_m = sample_embeddings.size(1) // 16
    quantized_default = quantize(sample_embeddings)
    
    # Lower M (more compression, less accuracy)
    lower_m = max(1, default_m // 2)
    quantized_low_m = quantize(sample_embeddings, m=lower_m)
    
    # Higher M (less compression, more accuracy)
    higher_m = default_m * 2
    quantized_high_m = quantize(sample_embeddings, m=higher_m)
    
    # Check shapes match
    assert quantized_default.shape == sample_embeddings.shape
    assert quantized_low_m.shape == sample_embeddings.shape
    assert quantized_high_m.shape == sample_embeddings.shape
    
    # Compare similarities
    cos_sim_default = torch.nn.functional.cosine_similarity(
        sample_embeddings.view(-1), quantized_default.view(-1), dim=0
    )
    cos_sim_low_m = torch.nn.functional.cosine_similarity(
        sample_embeddings.view(-1), quantized_low_m.view(-1), dim=0
    )
    cos_sim_high_m = torch.nn.functional.cosine_similarity(
        sample_embeddings.view(-1), quantized_high_m.view(-1), dim=0
    )
    
    print("[Cos] default", cos_sim_default)
    print("[Cos] low_m", cos_sim_low_m)
    print("[Cos] high_m", cos_sim_high_m)
    # Higher M should give better quality (higher similarity)
    assert cos_sim_high_m > cos_sim_default, "Higher M should give better accuracy"
    assert cos_sim_default > cos_sim_low_m, "Lower M should give worse accuracy"


def test_save_load_with_tempfile(sample_embeddings):
    """Test save and load functionality using a temporary file"""
    with tempfile.NamedTemporaryFile(suffix='.ezip', delete=False) as tmp:
        temp_path = tmp.name
        try:
            # Save to temporary file
            print(f"Saving emb of shape {sample_embeddings.shape} to {temp_path}")
            save(sample_embeddings, temp_path)
            
            # Check file exists and is not empty
            assert os.path.exists(temp_path)
            assert os.path.getsize(temp_path) > 0
            
            # Load from temporary file
            loaded = load(temp_path)
            
            # Check shapes match
            assert loaded.shape == sample_embeddings.shape
            
            # Check cosine similarity
            cos_sim = torch.nn.functional.cosine_similarity(
                sample_embeddings.view(-1), loaded.view(-1), dim=0
            )
            assert 0.5 < cos_sim < 1.0, f"Cosine similarity {cos_sim} out of expected range"
        finally:
            # Clean up the temporary file
            if os.path.exists(temp_path):
                os.unlink(temp_path)


@pytest.mark.parametrize("m", [24, 48, 96])
def test_save_load_custom_m(sample_embeddings, m):
    """Test save and load functionality with different M values"""
    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = Path(temp_dir) / f"embeddings_m{m}.ezip"
        
        # Save with custom M
        save(sample_embeddings, str(file_path), m=m)
        
        # Load the saved file
        loaded = load(str(file_path))
        
        # Check shapes match
        assert loaded.shape == sample_embeddings.shape
        
        # Check cosine similarity
        cos_sim = torch.nn.functional.cosine_similarity(
            sample_embeddings.view(-1), loaded.view(-1), dim=0
        )
        assert 0.5 < cos_sim < 1.0, f"Cosine similarity {cos_sim} out of expected range with m={m}"
