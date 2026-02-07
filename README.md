<img src="https://github.com/dbjzs/SpaLP/blob/main/Logo.svg" width="150"  alt="SpaLP-logo">

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/dbjzs/SpaLP/blob/main/LICENSE)
[![Stars](https://img.shields.io/github/stars/dbjzs/SpaLP?logo=GitHub&color=yellow)](https://github.com/dbjzs/SpaLP/stargazers)
[![Docs](https://readthedocs.org/projects/SpaLP/badge/?version=latest)](https://spalp.readthedocs.io/en/latest/index.html)
[![Forks](https://img.shields.io/github/forks/dbjzs/SpaLP?logo=GitHub&color=yellow)](https://github.com/dbjzs/SpaLP/forks)
![Python 3.10.13](https://img.shields.io/badge/python->=3.10-blue.svg)


SpaLP (**Spa**tial **L**ocal **P**ooling) is a python package for ultra-large-scale spatial omics data, including spatial atlas building, niche identification, omics data reconstruction, multi-slice integration (within-platform & cross-platform), large-scale multi-omics integration, cross-platform generalized and zero-shot learning.  

## Installation
#### 📥 Download
```
git clone https://github.com/dbjzs/SpaLP.git
cd SpaLP
```
#### 🔧 environment
SpaLP is available for Python 3.10. We recommend to train SpaLP models on a device with GPU support.  
* Using the conda install environment
```
conda create -n SpaLP -c conda-forge python==3.10.13 libopenblas=0.3.25 -y
conda activate SpaLP
```
#### 🛠️package
* Then using pip install SpaLP.
```
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install .
```

### 🚀Getting started Tutorial
- Tutorials and API documentation are available at [Tutorial](https://spalp.readthedocs.io/en/latest/index.html).
- Please use [issues](https://github.com/dbjzs/SpaLP/issues) to submit bug reports.
- All experiments were performed on a NVIDIA A800-SXM4-80 GB GPU and Intel(R) Xeon(R) Platinum 8462Y+(32 cores) CPU.
- According to the tutorial, running SpaLP should < 1 minute on most datasets with million cells.

### 📁 Tutorial h5ad file
- All h5ad files have been uploaded to the [zenodo repository](https://zenodo.org/records/18483604)


### Reference
- If you find SpaLP useful for your research, please consider citing the SpaLP manuscript [bioRxiv](https://www.biorxiv.org/cgi/content/short/2026.02.04.703814v1).

```
@article{Dai2026.02.04.703814,
  title = {A lightweight, ultrafast and general embedding framework for large-scale spatial omics data},
  author = {Dai, et al.},
  year = {2026},
  journal = {bioRxiv : the preprint server for biology},
  eprint = {https://www.biorxiv.org/cgi/content/short/2026.02.04.703814v1},
  doi = {https://doi.org/10.64898/2026.02.04.703814},
}
```

 

### ⏱️ Experimental configuration and running time
All experiments were performed on a NVIDIA A800-SXM4-80 GB GPU and Intel(R) Xeon(R) Platinum 8462Y+(32 cores) CPU.
####  Fig2

|   Title                     | Cells                     |Genes/Protenis| SpaLP Runtime|Platform|
|-----------------------------|---------------------------|------|-------------|-------------|
| 640,000 cells Simulation data |640,000|31,493 genes|52s|Simulation|
| Xenium Breast Cancer Data     |167,780|313 genes|7s|Xenium|
| CosMx Mouse Brain     | 48,180 |950 genes|7s|CosMx|

###  Fig3
|   Title                     |  Cells                     |Genes/Protenis| SpaLP Runtime|Platform|
|-----------------------------|-----------|------|-------------|-------------|
| 1.35Million Mouse_Tissue     | 1,355,849|379 genes|47s|Xenium|
| Stereo-seq mouse testes     | 198,248|27,869 genes|24s|Stereo-seq V1.3|
| Stereo CITE-seq mouse spleen     | 295,215|128 proteins|14s|Stereo CITE-seq|

###  Fig4
+ within-platform integration

|   Title                     |  Cells                     |Genes/Protenis| SpaLP Runtime|Platform|
|-----------------------------|-----|------|-------------|-------------|
| Coronal mouse brain | 734,696|483 genes|47s|MERSCOPE|
| Sagittal mouse brain | 91,246|1022 genes|30s|STARmap PLUS|
| Sagittal mouse brain | 123,836|1022 genes|30s|STARmap PLUS|
| Sagittal mouse brain | 207,591|1022 genes|30s|STARmap PLUS|
|  VisiumHD Tonsil | 553,820|18,085 genes|44s|Visium HD|
|  VisiumHD Tonsil | 679,294|18,085 genes|44s|Visium HD|


+ Cross-platform integration

|   Title                     |  Cells                     |Genes/Protenis| SpaLP Runtime|Platform|
|-----------------------------|-------------|------|-------------|-------------|
| Cross-platform Mouse Brain  | 49,430|1122 genes|7s|MERFISH|
| Cross-platform Mouse Brain  | 43,341|1022 genes|7s|STARmapPLUS|
| Cross-platform Mouse Brain  | 48,180|950 genes|7s|CosMx|
| Cross-platform colorectal cancer |493,834|10000 genes|57s|CosMx|
| Cross-platform colorectal cancer | 307,762|422 genes|57s|Xenium|
| Cross-platform colorectal cancer | 507,684|18,085 genes|57s|Visium HD|
| Cross-platform colorectal cancer | 545,913|18,085 genes|57s|Visium HD|
| Cross-platform colorectal cancer | 541,968|18,085 genes|57s|Visium HD|


###  Fig5
|   Title                     |  Cells                     |Genes/Protenis| SpaLP Runtime|Platform|
|-----------------------------|------------|------|-------------|-------------|
| 8.4 million cells Mouse Brain Atlas     | 4,167,869|1122 genes|3min 41s|MERFISH|
| 8.4 million cells Mouse Brain Atlas     |1,915,592|1122 genes|3min 41s|MERFISH|
| 8.4 million cells Mouse Brain Atlas     | 2,081,549|1122 genes|3min 41s|MERFISH|
| 8.4 million cells Mouse Brain Atlas     | 215,278|1122 genes|3min 41s|MERFISH|

###  Fig6
|   Title                     | Cells                     |Genes/Protenis| SpaLP Runtime|Platform|
|-----------------------------|---------------|------|-------------|-------------|
| CosMx Kidney cancer self-house data   | 1,236,281|1000 genes|1min 03s|CosMx|
| Xenium gastric cancer     | 696,314|377 genes|36s|Xenium|
| Xenium multi-omics renal cell carcinoma     | 465,545|396 genes |28s|Xenium|
| Xenium multi-omics renal cell carcinoma     | 465,545|27 proteins |28s|Xenium|


###  Fig7
|   Title                     |  Cells                     |Genes/Protenis| SpaLP Runtime|Platform|
|-----------------------------|---------|------|-------------|-------------|
| Pre-training data     | 49,430|1122 genes|7s|MERFISH|
| Pre-training data     |43,341|1022 genes|7s|STARmapPLUS|
| Pre-training data     |48,180|950 genes|7s|CosMx|
| Inference data     | 48,180|1122 genes|1s|C57BL6J-2.041|
| Inference data     |70,035|~28,000 genes|1s|Stereo-seq|



###  Exntend Data Fig3
|   Title                     |  Cells                     |Genes/Protenis| SpaLP Runtime|Platform|
|-----------------------------|-----------------|------|-------------|-------------|
| CODEX mouse spleen     | 82,251|30 proteins|13s|CODEX|
| CODEX mouse spleen     | 81,346|30 proteins|12s|CODEX|
| CODEX mouse spleen     | 80,636|30 proteins|12s|CODEX|





