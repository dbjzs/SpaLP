<img src="https://github.com/dbjzs/SpaLP/blob/main/Logo.svg" width="150"  alt="SpaLP-logo">

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/dbjzs/SpaLP/blob/main/LICENSE)
[![Stars](https://img.shields.io/github/stars/dbjzs/SpaLP?logo=GitHub&color=yellow)](https://github.com/dbjzs/SpaLP/stargazers)
[![Docs](https://readthedocs.org/projects/SpaLP/badge/?version=latest)](https://spalp.readthedocs.io/en/latest/index.html)
[![Forks](https://img.shields.io/github/forks/dbjzs/SpaLP?logo=GitHub&color=yellow)](https://github.com/dbjzs/SpaLP/forks)
[![PyPI Downloads](https://img.shields.io/pepy/dt/spalp?logo=pypi)](https://pepy.tech/project/spalp)
[![PyPI - Version](https://img.shields.io/pypi/v/spalp?logo=pypi)](https://pypi.org/project/spalp/)
[![Zenodo Downloads](https://img.shields.io/badge/dynamic/json?color=blue&label=Zenodo%20Downloads&query=$.stats.unique_downloads&url=https://zenodo.org/api/records/18483604)](https://zenodo.org/record/18483604)
![Python 3.10.13](https://img.shields.io/badge/python->=3.10-blue.svg)


SpaLP (**Spa**tial **L**ocal **P**ooling) is a python package for ultra-large-scale spatial omics data, including spatial atlas building, niche identification, omics data reconstruction, multi-slice integration (within-platform & cross-platform), large-scale multi-omics integration, cross-platform generalized and zero-shot learning.  

## Installation via Github
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

## Installation via PyPi
#### 🔧 environment
SpaLP is available for Python 3.10. We recommend to train SpaLP models on a device with GPU support.  
* Using the conda install environment
```
conda create -n SpaLP -c conda-forge python==3.10.13 libopenblas=0.3.25 -y
conda activate SpaLP
```
#### 🛠️package
* Then install SpaLP.
```
pip install SpaLP
```

### 📁 Tutorial h5ad file
- All h5ad files have been uploaded to the [zenodo repository](https://zenodo.org/records/18483604)
  
### 🚀Getting started Tutorial
- Jupyter tutorials and API documentation are available at [Tutorial](https://spalp.readthedocs.io/en/latest/index.html).
- Command line usage
- The expected data input format of SpaLP is [AnnData](https://anndata.readthedocs.io/en/stable/) object.  
  The user needs to store the two-dimensional coordinates of the slices in the "obsm" variable and name it "spatial".  
  The preprocessed feature matrix needs to be stored in the "obsm" variable and named as "feat".
  ```
   adata.obsm['spatial']: spatial coordinates
   adata.obsm['feat']: feature matrix (cells × genes)  
  ```
- Preprocessing steps  
  For the original count matrix
  ```
   sc.pp.normalize_total(adata, inplace=True)  
   sc.pp.log1p(adata)
   sc.pp.scale(adata)  
   adata.obsm['feat'] = adata.X  
  ```
  For log-transformed expression matrix or protein data
  ```
   sc.pp.scale(adata) 
   adata.obsm['feat'] = adata.X 
  ```
  For the technology platform with more than 3000 genes, we recommend using top2000 or top3000 highly variable genes.
  ```
   sc.pp.highly_variable_genes(adata, n_top_genes=2000, flavor='seurat_v3')
   adata = adata[:,adata.var.highly_variable]
   sc.pp.normalize_total(adata, inplace=True)
   sc.pp.log1p(adata)
   sc.pp.scale(adata)
   adata.obsm['feat'] = adata.X
  ```
  For technical platforms with gene panels less than 2000, we recommend using all genes as input. 
- Please use [issues](https://github.com/dbjzs/SpaLP/issues) to submit bug reports.
  
  
### 🖥️ Computing resources and running time
- All experiments in the manuscript were performed on a NVIDIA A800-SXM4-80 GB GPU and Intel(R) Xeon(R) Platinum 8462Y+(32 cores) CPU.
- According to the tutorial, running time for the same configuration should < 1 minute on most datasets with million cells.
- SpaLP requires that the computing device must have at least 1 CPU core.
- The requirements for GPU memory and CPU memory of SpaLP are listed in the following table.
  
| Cells                     |input genes/proteins|Platform|GPUmemory|CPUmemory|Reference running time|K-nearest neighbor|
|---------------------------|------|-------------|-------------|---------|---------|---------|
|2,127,707|329 genes|cross-platform|21.96GB|36GB|1min 02s|4|
|1,355,849|379 genes|Xenium|15.89GB|4.49GB|47s|3|
|1,236,281|1000 genes|CosMx|30.15GB|8.07GB|1min 03s|4|
|696,314|377 genes|Xenium|13.41GB|3.24GB|39s|5|
|640,000|2000 genes|Simulation|29.68GB|7.87GB|52s|5|
|422,673|1022 genes|STARmapPLUS|14.85GB|6.22GB|34s|6|
|167,780|313 genes|Xenium|2.01GB|1.59GB|7s|3|
|48,180 |950 genes|CosMx|1.85GB|0.26GB|7s|8|
|1,395,992|43 proteins|CODEX|5.29GB|3.81GB|25s|4|
|295,215|128 proteins|Stereo-CITE-seq|4.04GB|1.44GB|15s|4|


- For 3 million cells or more, see the 8.4 million integration tutorial.




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






