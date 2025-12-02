## SpaLP
A novel, ultrafast and general embedding framework for large-scale spatial omics

### Tutorial
All the result tutorials mentioned in the text can be found [Tutorial](https://spalp.readthedocs.io/en/latest/index.html)

### All h5ad file in Tutorial
Fig2:[simulatedata.h5ad](https://drive.google.com/open?id=1DnPjxTxS6fLjWtfio__s_yMvgp0zqqhS&usp=drive_fs) 
     [Xenium_Breast_Cancer.h5ad](https://drive.google.com/open?id=1StPUArtCFN0oyQLoKN6gQ8n9WlWIAkDl&usp=drive_fs) 
     [CosMxMouseBrain.h5ad](https://drive.google.com/open?id=11aHibK5ZpmI7Ogoru2Y3vDMafP4TTP11&usp=drive_fs)



### Install
```
conda create -n SpaLP -c conda-forge python==3.10.13 libopenblas=0.3.25 -y
conda activate SpaLP
cd SpaLP
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install .
```
