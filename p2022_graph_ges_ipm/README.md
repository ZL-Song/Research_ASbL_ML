# Edge-Conditioned Graph-Learning for Understanding GES-5/Imipenem Deacylation.
This data repository contains all necessary files to replicate the graph-learning part of the study noted in the description.

# Graph-Learning (3.gnn dir)

## Dependencies for the graph-learning
- pytorch >= 1.9.0
- pytorch_geometric >= 2.0.3
- Numpy

An conda environment file (environment.yml) is attached for setting up the graph learning environments.

## Running the code in 3.gnn dir.

0. Make necessary directories.
```bash
cd 3.gnn
mkdir -p data_split model_latent model_latent_pert model_mpnn model_pred
```

1. Split the data into training and validation.
Note that one need to change the "_basedir" var to get compatible base directory specs.
```bash
python io_gesdata.py
```

2. Model training.
```bash
python train.py
```

3. Predict the energy barriers for each data point.
```bash
python test_all.py
```

4. Record the latent vectors for each data point.
```bash
python test_latent.py
```

5. Record the latent displacements for each data point upon each edge absence.
```bash
python pert_latent.py
```

All necessary data is presented in the directories made in step 0.

## Explanation to other files
- 2.dataset/*py: This directory holds all python files that are used preprocess the QM/MM geometries and data files (using MDAnalysis, any version). The indices in the file names note the order of execution of those files, necessary comments are noted within those codes;
- 2.dataset/iomisc.py: This file groups a series of convienient functions that are used to load the data, one needs to change the function basedir() and other necessary dir setting functions to properly set up the scripts in this directory;
- 2.dataset/selection.py: This file implements the functions to do atom/angle/dihedral selections with MDAnalysis;
- 3.gnn/mpnn.py: Implements the ECGCNN model;
- 3.gnn/test.py: Makes predictions and group them into the training and validation sets, for later ploting purposes.  
- Files in dir p.figures: All figures presented in the study are plotted with Jupyter notebooks and matplotlib (any version). The metadata are saved as Numpy arrays in dirs 2.dataset and 3.gnn.