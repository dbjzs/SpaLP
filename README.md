## SpaLP
A novel, ultrafast and general embedding framework for large-scale spatial omics

### Tutorial
All the result tutorials mentioned in the text can be found [Tutorial](https://spalp.readthedocs.io/en/latest/index.html)

### All h5ad file in Tutorial
#### Fig2
640,000 cells Simulation data [simulatedata.h5ad](https://drive.google.com/open?id=1DnPjxTxS6fLjWtfio__s_yMvgp0zqqhS&usp=drive_fs)  
Xenium Breast Cancer Data [Xenium_Breast_Cancer.h5ad](https://drive.google.com/open?id=1StPUArtCFN0oyQLoKN6gQ8n9WlWIAkDl&usp=drive_fs)  
CosMx Mouse Brain [CosMxMouseBrain.h5ad](https://drive.google.com/open?id=11aHibK5ZpmI7Ogoru2Y3vDMafP4TTP11&usp=drive_fs)
#### Fig3
1.35Million Mouse_Tissue [Million_Mouse_Tissue.h5ad](https://drive.google.com/open?id=10XtS2L9UgGLqnkPBhJ6UIYdgZ5BICwp5&usp=drive_fs)  
Stereo-seq mouse testes [testis.h5ad](https://drive.google.com/open?id=1li92sr3lFebNXjuAP1YOwMZzlKSOA66z&usp=drive_fs)  
Stereo CITE-seq mouse spleen [Stereo_CITE-seq.h5ad](https://drive.google.com/open?id=1VkSMlaeBz020JGZHxVNqW-MKDUmlAaS_&usp=drive_fs)
#### Fig4
Coronal mouse brain integration [merscope.h5ad](https://drive.google.com/open?id=15L9-qwdgLPdw6A8q2vMjY5nMCwu9J89w&usp=drive_fs)  
Sagittal mouse brain integration [starmap_plus_mouse_cns_batch1.h5ad](https://drive.google.com/open?id=12caAILqWOjDNKiaSYuz9-XMp3bN6CDjA&usp=drive_fs) , [starmap_plus_mouse_cns_batch2.h5ad](https://drive.google.com/open?id=1p3x0_JdCpcjV9AhusrW3OO-y-7lyPRcM&usp=drive_fs) and [starmap_plus_mouse_cns_batch3.h5ad](https://drive.google.com/open?id=1283gLKz04YuakzPnOZ72MF_ScCKGa_je&usp=drive_fs)  
VisiumHD Tonsil integration [FreshFrozenVisiumHDP1.h5ad](https://drive.google.com/open?id=16Hh1T34Cisj41x3QtRphtKG2dtsZ_CC-&usp=drive_fs) and [FFIFVisiumHDP2.h5ad](https://drive.google.com/open?id=11z920Equ8WV4dpPbNeVDCdvNoazT-Gbr&usp=drive_fs)  

Cross-platform Mouse Brain Integration [MERFISH.h5ad](https://drive.google.com/open?id=16UYRCGe6K5FAMYhoL2-2l7B8mYeCknQq&usp=drive_fs) , [STARmapPLUS.h5ad](https://drive.google.com/open?id=12cl4ToVZ8AosPshu_NVgmwegFUlY-Ol6&usp=drive_fs) and [CosMx.h5ad](https://drive.google.com/open?id=1qQRnL-zeWmzSZSlbxOiaKVtCFDB4xUW3&usp=drive_fs)





### Install
```
conda create -n SpaLP -c conda-forge python==3.10.13 libopenblas=0.3.25 -y
conda activate SpaLP
cd SpaLP
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install .
```
