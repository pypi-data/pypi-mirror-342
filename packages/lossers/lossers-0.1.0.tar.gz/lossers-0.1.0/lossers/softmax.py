import torch
from torch import nn
from torch.nn import functional as F_

def softmax_loss(input, target, **kwargs):
    return F_.cross_entropy(input, target, **kwargs)

class AMSoftmax(nn.Module):
    def __init__(self, in_dims, n_classes, m=0.35, s=30):
        super(AMSoftmax, self).__init__()
        self.m = m
        self.s = s
        self.in_dims = in_dims
        self.weight = nn.Parameter(torch.randn(n_classes, in_dims), requires_grad=True)
        nn.init.xavier_normal_(self.weight, gain=1)

    def forward(self, logits, labels):
        cosine = F_.linear(F_.normalize(logits), F_.normalize(self.weight))
        labels_view = labels.view(-1, 1)
        delta_cosine = torch.zeros_like(cosine).scatter_(1, labels_view, self.m)
        cosine_m = cosine - delta_cosine
        cosine_ms = self.s * cosine_m
        loss = F_.cross_entropy(cosine_ms, labels)
        return loss
