import torch
from torch.nn import functional as F_

def contrastive_loss(logits: torch.Tensor) -> torch.Tensor:
    return F_.cross_entropy(logits, torch.arange(len(logits), device=logits.device))

def clip_loss(similarity: torch.Tensor) -> torch.Tensor:
    caption_loss = contrastive_loss(similarity)
    image_loss = contrastive_loss(similarity.t())
    return (caption_loss + image_loss) / 2.0
