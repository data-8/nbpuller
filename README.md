# nbpuller
An extension for jupyter notebook to retrieve and update local files from remote git repository using native git pull and merge.

## Installation

You can currently install this directly from git:

```
pip install git+https://github.com/data-8/nbpuller.git
jupyter serverextension enable --py nbpuller
jupyter nbextension install --py nbpuller
```

To enable this extension for all notebooks:

```
jupyter nbextension enable --py nbpuller
```
