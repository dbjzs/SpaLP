import anndata
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

class MLP(nn.Module):
    def __init__(self, in_channels, out_channels, bn=False, activation_fn=None):
        super().__init__()
        self.linear = nn.Linear(in_channels, out_channels)
        self.bn = nn.BatchNorm1d(out_channels) if bn else None
        self.activation = activation_fn

    def forward(self, x):  # x: (bs, C_in)
        x = self.linear(x)  # (bs, C_out)
        if self.bn:
            x = self.bn(x)
        if self.activation:
            x = self.activation(x)
        return x  # (bs, C_out)

def batch_gather(data, index):
    return data[index]

def gather_neighbour(point_features, neighbor_idx):
    valid_mask = (neighbor_idx >= 0)  # (bs, k)
    neighbor_idx = torch.clamp(neighbor_idx, min=0)  
    
    gathered_features = batch_gather(point_features, neighbor_idx)  # (bs, k, C)
    gathered_features = gathered_features * valid_mask.unsqueeze(-1).float()
    
    return gathered_features

class AttentivePooling(nn.Module):
    def __init__(self, in_channels, out_channels):
        super().__init__()
        self.score_fn = nn.Sequential(
            nn.Linear(in_channels, in_channels, bias=False),
            nn.Softmax(dim=1)  # softmax over k
        )
        self.mlp = MLP(in_channels, out_channels, bn=False, activation_fn=None)

    def forward(self, x):  # x: (bs, k, C)
        scores = self.score_fn(x)  # (bs, k, C)
        feat = torch.sum(scores * x, dim=1)  # (bs, C)
        return self.mlp(feat)  # (bs, C_out)

class LocalFeatureAggregation(nn.Module):
    def __init__(self, in_channels, out_channels):
        super().__init__()
        self.mlp1 = MLP(in_channels, 2*out_channels, bn=False, activation_fn=nn.ReLU())
        self.bn_after_gather = nn.LayerNorm(2*out_channels)
        self.pool1 = AttentivePooling(2*out_channels, out_channels)

    def forward(self, features, neighbor_idx):
        x = self.mlp1(features)  # (bs, 2*out_channels)
        x = gather_neighbour(x, neighbor_idx)  # (bs, k, 2*out_channels) 

        x = self.bn_after_gather(x) 
        x = self.pool1(x)  # (bs, out_channels)
        return x

class Decoder(nn.Module):
    def __init__(self, in_channels, out_channels, bn=False, activation_fn=nn.ReLU()):
        super().__init__()
        self.mlp = MLP(in_channels, out_channels, bn=bn, activation_fn=activation_fn)

    def forward(self, x):  # x: (bs, C)
        return self.mlp(x)

class SpatialLocalPooling_batch(nn.Module):
    def __init__(self, in_channels, out_channels):
        super().__init__()
        self.encoder = LocalFeatureAggregation(in_channels, out_channels)
        self.decoder = Decoder(out_channels, in_channels, bn=False, activation_fn=nn.ReLU())

    def forward(self, features, neighbor_idx):
        embedding = self.encoder(features, neighbor_idx)  # (bs, C_mid)
        reconstructed = self.decoder(embedding)  # (bs, C_in)
        return reconstructed, embedding
