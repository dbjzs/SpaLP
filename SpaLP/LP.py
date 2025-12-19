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

    def forward(self, x):  # x: (N, C_in)
        x = self.linear(x)  # (N, C_out)
        if self.bn:
            x = self.bn(x)
        if self.activation:
            x = self.activation(x)
        return x  # (N, C_out)


def batch_gather(data, index):
    return data[index]


def gather_neighbour(point_features, neighbor_idx):
    point_features_t = point_features
    gathered_features = batch_gather(point_features_t, neighbor_idx)
    return gathered_features


class AttentivePooling(nn.Module):
    def __init__(self, in_channels, out_channels):
        super().__init__()
        self.score_fn = nn.Sequential(
            nn.Linear(in_channels, in_channels, bias=False),
            nn.Softmax(dim=1)  # softmax over k (neighbor dim)
        )
        self.mlp = MLP(in_channels, out_channels, bn=False, activation_fn=None)

    def forward(self, x):  # x: (N, k, C)
        scores = self.score_fn(x)  # (N, k, C)
        
        feat = torch.sum(scores * x, dim=1)  # (N, C)
        return self.mlp(feat)  # (N, C_out)

class LocalFeatureAggregation(nn.Module):
    def __init__(self, in_channels, out_channels):
        super().__init__()
        self.mlp1 = MLP(in_channels, 2*out_channels, bn=False, activation_fn=nn.ReLU())
        self.bn_after_gather = nn.BatchNorm1d(2*out_channels)
        self.pool1 = AttentivePooling(2*out_channels, out_channels)

    def forward(self, features, neighbor_idx):
        """
        coords: (N, coord_dim)
        features: (N, C_in)
        neighbor_idx: (N, k)
        """
        x = self.mlp1(features)  # (N, 128)
        x = gather_neighbour(x, neighbor_idx)#(N, k, 128)

        x = x.permute(0, 2, 1)  
        x = self.bn_after_gather(x) 
        x = x.permute(0, 2, 1)
        
        x = self.pool1(x)  # (N, out_channels)
        return x

class Decoder(nn.Module):
    def __init__(self, in_channels, out_channels, bn=False, activation_fn=nn.ReLU()):
        super().__init__()
        self.mlp = MLP(in_channels, out_channels, bn=bn, activation_fn=activation_fn)

    def forward(self, x):  # x: (N, C)
        return self.mlp(x)

class SpatialLocalPooling(nn.Module):
    def __init__(self, in_channels, out_channels):
        super().__init__()
        self.encoder = LocalFeatureAggregation(in_channels, out_channels)
        self.decoder = Decoder(out_channels, in_channels, bn=False, activation_fn=nn.ReLU())

    def forward(self, features, neighbor_idx):
        """
        coords: (N, coord_dim)
        features: (N, C_in)
        neighbor_idx: (N, k)
        """
        embedding = self.encoder(features, neighbor_idx)  # (N, C_mid)
        reconstructed = self.decoder(embedding)  # (N, C_in)
        return reconstructed, embedding
