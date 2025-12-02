# SpaLP
A novel, ultrafast and general embedding framework for large-scale spatial omics


## Installation
SpaLP is available for Python 3.10. We recommend to train SpaLP models on a device with GPU support.  
We recommend using the conda installation environment
```
conda create -n SpaLP -c conda-forge python==3.10.13 libopenblas=0.3.25 -y
conda activate SpaLP
```
Then install SpaLP using pip.
```
cd SpaLP
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install .
```

## Dependencies
You'll need to install the following packages in order to run the codes.
* Python==3.10.13
* libopenblas==0.3.25
* scanpy==1.9.8
* torch==2.2.0
* torch_geometric==2.4.0
* scipy==1.12.0
* pandas==2.2.3
* scikit-learn==1.4.0
* numpy==1.26.3
* numba==0.59.0
* llvmlite==0.42.0
* anndata==0.10.5.post1
* leidenalg==0.10.2
* igraph==0.11.8
* scikit-misc==0.5.1

See full list in requirements.txt file. SpaLP can be run on CPU or GPU.


## Tutorial
Check out our readthedocs, which includes tutorials for four analyses:  
All the result tutorials mentioned in the text can be found [Tutorial](https://spalp.readthedocs.io/en/latest/index.html)  

Training SpaLP by following the tutorials should take <1 minute.  
## Data
In this paper, we tested 1 simulation datasets and 18 

### Fig2
* 640,000 cells Simulation data [simulatedata.h5ad](https://drive.google.com/open?id=1DnPjxTxS6fLjWtfio__s_yMvgp0zqqhS&usp=drive_fs)  
Xenium Breast Cancer Data [Xenium_Breast_Cancer.h5ad](https://drive.google.com/open?id=1StPUArtCFN0oyQLoKN6gQ8n9WlWIAkDl&usp=drive_fs)  
CosMx Mouse Brain [CosMxMouseBrain.h5ad](https://drive.google.com/open?id=11aHibK5ZpmI7Ogoru2Y3vDMafP4TTP11&usp=drive_fs)
### Fig3
1.35Million Mouse_Tissue [Million_Mouse_Tissue.h5ad](https://drive.google.com/open?id=10XtS2L9UgGLqnkPBhJ6UIYdgZ5BICwp5&usp=drive_fs)  
Stereo-seq mouse testes [testis.h5ad](https://drive.google.com/open?id=1li92sr3lFebNXjuAP1YOwMZzlKSOA66z&usp=drive_fs)  
Stereo CITE-seq mouse spleen [Stereo_CITE-seq.h5ad](https://drive.google.com/open?id=1VkSMlaeBz020JGZHxVNqW-MKDUmlAaS_&usp=drive_fs)
### Fig4
Coronal mouse brain integration [merscope.h5ad](https://drive.google.com/open?id=15L9-qwdgLPdw6A8q2vMjY5nMCwu9J89w&usp=drive_fs)  
Sagittal mouse brain integration [starmap_plus_mouse_cns_batch1.h5ad](https://drive.google.com/open?id=12caAILqWOjDNKiaSYuz9-XMp3bN6CDjA&usp=drive_fs) , [starmap_plus_mouse_cns_batch2.h5ad](https://drive.google.com/open?id=1p3x0_JdCpcjV9AhusrW3OO-y-7lyPRcM&usp=drive_fs) and [starmap_plus_mouse_cns_batch3.h5ad](https://drive.google.com/open?id=1283gLKz04YuakzPnOZ72MF_ScCKGa_je&usp=drive_fs)  
VisiumHD Tonsil integration [FreshFrozenVisiumHDP1.h5ad](https://drive.google.com/open?id=16Hh1T34Cisj41x3QtRphtKG2dtsZ_CC-&usp=drive_fs) and [FFIFVisiumHDP2.h5ad](https://drive.google.com/open?id=11z920Equ8WV4dpPbNeVDCdvNoazT-Gbr&usp=drive_fs)  

Cross-platform Mouse Brain Integration [MERFISH.h5ad](https://drive.google.com/open?id=16UYRCGe6K5FAMYhoL2-2l7B8mYeCknQq&usp=drive_fs) , [STARmapPLUS.h5ad](https://drive.google.com/open?id=12cl4ToVZ8AosPshu_NVgmwegFUlY-Ol6&usp=drive_fs) and [CosMx.h5ad](https://drive.google.com/open?id=1qQRnL-zeWmzSZSlbxOiaKVtCFDB4xUW3&usp=drive_fs)  
Cross-platform colorectal cancer integration [CosMx.h5ad](https://drive.google.com/open?id=1IFnZ6zLNpIe9edVPiVAlktSmQBUFxcEc&usp=drive_fs) , [Xeniump1.h5ad](https://drive.google.com/open?id=1k6F_FSWnOVQWhgszttQduiTMl5ULA0AC&usp=drive_fs) , [VisiumHD_P1.h5ad](https://drive.google.com/file/d/1OX_feTaU8NYL9_CFjQIGG4jrN-slvknT/view?usp=sharing) , [VisiumHD_P2.h5ad](https://drive.google.com/file/d/1qDWPERNYxaKzYZQd9wG0or2g0SKiKNtX/view?usp=drive_link) and [VisiumHD_P5.h5ad](https://drive.google.com/file/d/1Rs_BJ2Q9rankWc5zemj0Qbt0Q5fv0bnj/view?usp=drive_link)



## Installation
```
conda create -n SpaLP -c conda-forge python==3.10.13 libopenblas=0.3.25 -y
conda activate SpaLP
cd SpaLP
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install .
```
