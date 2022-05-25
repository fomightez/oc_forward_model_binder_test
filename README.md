# OC_forward_model

Translation of excel based ocean colour forward modelling approaches from Ruddick and Bernard into a consolidated python-based module

## Use

The model is consists of a modular toolkit (in python) and an extremelt simple Jupyter Notebook frontend implementation. We recommedn installting the package using the Anaconda package manager. The package can be installed as follows

`git clone https://gitlab.com/benloveday/oc_forward_model.git` \
`cd oc_forward_model` \
`conda env create -f environment.yml` \
`conda activate oc_forward` \
`jupyter-notebook` \

Once the notebook server is running, you should run the `Run_model.ipynb` notebook

## To do

* Add Bernard at al. effective diamater and dual algal populations
* homogenise Ruddick and Bernard LUTs...possible or dual model?
* Add OLCI, MSI, FCI "extractions" at specified wavelengths and with relevant SRFs
* "idealised" atmosphere addition? Sreerekha RT-TOV?