import anndata
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from tqdm import tqdm
from .utils import set_seed

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

        
    def Train(self,graph,epochs=200,lr=1e-3,device=None,seed=7,mode="single-slice"):
        """
        Train the modelgraph:
        - Single Graph object
        - OR list of Graph objects (multi-slices)
        """
        set_seed(seed)
        self.to(device)
            
        optimizer = optim.Adam(self.parameters(), lr=lr)
        criterion = nn.MSELoss()
        losses = []
        # =========================
        # Single-slice training
        # =========================
        if mode == "single-slice":
            self.train()
            pbar = tqdm(range(epochs), desc="Training(single-slices)", ncols=200)
            for epoch in pbar:
                peak = torch.cuda.max_memory_allocated(device) / 1024**3
                optimizer.zero_grad()
                reconstructed,embedding = self(graph.features, graph.neighbor_idx)
                loss = criterion(reconstructed, graph.features)
                loss.backward()
                optimizer.step()
                losses.append(loss.item())
                pbar.set_postfix({"Epoch": epoch,"Loss": f"{loss.item():.4f}","PeakGPUmemory": f"{peak:.2f}GB"})
                
        # =========================
        # multi-slice training
        # =========================
        elif mode == "multi-slices":
            set_seed(seed)
            self.train()
            pbar = tqdm(range(epochs), desc="Training(multi-slices)", ncols=200)
            for epoch in pbar:
                total_loss = 0.0
                num_batches = 0
                for g in graph:  # graph is a list of Graphs
                    features = g.features.to(device)
                    neighbor_idx = g.neighbor_idx.to(device)
                    optimizer.zero_grad()
                    reconstructed, embedding = self(features, neighbor_idx)
                    loss = criterion(reconstructed, features)
                    loss.backward()
                    optimizer.step()
                    total_loss += loss.item()
                    num_batches += 1
                avg_loss = total_loss / max(num_batches, 1)
                losses.append(avg_loss)
                peak = torch.cuda.max_memory_allocated(device) / 1024**3
                pbar.set_postfix({"Epoch": epoch,"Avg Loss": f"{avg_loss:.4f}","PeakGPUmemory": f"{peak:.2f}GB"})

        else:
            raise ValueError('mode must be "single-slice" or "multi-slices"')
                
            
        
    @torch.no_grad()
    def get_embedding(self, graph,mode="single-slice",device=None):
        """
        Get embedding after training
        """
        if mode == "single-slice":
            self.eval()
            reconstructed, embedding = self(graph.features,graph.neighbor_idx)
            return reconstructed.cpu().numpy(), embedding.cpu().numpy()

        elif mode == "multi-slices":
            all_recon = []
            all_emb = []
            for g in graph:  # graph is a list
                features = g.features.to(device)
                neighbor_idx = g.neighbor_idx.to(device)
                reconstructed, embedding = self(features, neighbor_idx)
    
                all_recon.append(reconstructed.cpu())
                all_emb.append(embedding.cpu())
    
            full_recon = torch.cat(all_recon, dim=0)
            full_emb = torch.cat(all_emb, dim=0)
            return full_recon.numpy(), full_emb.numpy()
        else:
            raise ValueError('mode must be "single-slice" or "multi-slices"')