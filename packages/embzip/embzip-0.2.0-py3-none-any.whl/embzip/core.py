from typing import Optional

import lzma

import torch
import faiss
import os
import pickle


def quantize(embeddings: torch.Tensor, m: Optional[int] = None, nbits: int = 4) -> torch.Tensor:
    """
    Quantize embeddings using Product Quantization (PQ).
    
    Args:
        embeddings: Input embeddings tensor
        m: Number of sub-quantizers to use (default: dimension/16)
        nbits: Number of bits per sub-quantizer (default: 4)
    
    Returns:
        Quantized embeddings tensor
    """ 
    d = embeddings.size(1)
    if m is None:
        m = d // 16
        
    index = faiss.index_factory(
        d, f"IDMap2,PQ{m}x{nbits}", faiss.METRIC_INNER_PRODUCT
    )
    # TODO: Quiet warning
    # index.cp.min_points_per_centroid = 5   # quiet warning
    index.train(embeddings.cpu())
    code = index.index.sa_encode(embeddings.cpu().numpy())
    return torch.tensor(index.index.sa_decode(code))


def save(embeddings: torch.Tensor, path: str, m: Optional[int] = None, nbits: int = 4) -> None:
    """
    Compress and save embeddings to a file.
    
    Args:
        embeddings: Embeddings tensor to save
        path: Output file path
        m: Number of sub-quantizers to use (default: dimension/16)
        nbits: Number of bits per sub-quantizer (default: 4)
    """
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(os.path.abspath(path)) or '.', exist_ok=True)
    
    d = embeddings.size(1)
    if m is None:
        m = d // 16
    
    # Create and train the index
    index = faiss.index_factory(
        d, f"IDMap2,PQ{m}x{nbits}", faiss.METRIC_INNER_PRODUCT
    )
    # TODO: Quiet warning
    # index.cp.min_points_per_centroid = 5   # quiet warning
    index.train(embeddings.cpu())
    
    # Add IDs and embeddings to the index
    ids = torch.arange(len(embeddings)).numpy()
    index.add_with_ids(embeddings.cpu().numpy(), ids)
    
    # Encode embeddings
    codes = index.index.sa_encode(embeddings.cpu().numpy())
    
    # Save the index configuration, codes, and metadata
    data = {
        'codes': codes,
        'index': index,
        'shape': embeddings.shape,
        'm': m,
        'nbits': nbits
    }
    
    with lzma.open(path, 'wb') as f:
        pickle.dump(data, f)

def load(path: str) -> torch.Tensor:
    """
    Load and decompress embeddings from a file.
    
    Args:
        path: Input file path
    
    Returns:
        Reconstructed embeddings tensor
    """
    with lzma.open(path, 'rb') as f:
        data = pickle.load(f)
    
    codes = data['codes']
    index = data['index']
    
    return torch.tensor(index.index.sa_decode(codes)) 