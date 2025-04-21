import torch

def estimate_tensor_size_bytes(tensor: torch.Tensor) -> int:
    return tensor.element_size() * tensor.numel()
