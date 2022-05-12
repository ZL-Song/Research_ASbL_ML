# Make predictions with a MPNN model on all dataset with ordered data entries.
# Zilin Song, 20 Mar 2022
# 
import io_gesdata, mpnn
import numpy

import torch
import torch.nn.functional as F

from torch_geometric.loader import DataLoader

if __name__ == '__main__':
    # ---
    # Load data list.
    d1, d2 = io_gesdata.load_ges_data(split=False)

    # ---
    # Make data loaders
    d1_loader = DataLoader(d1, batch_size=25, shuffle=False)
    d2_loader = DataLoader(d2, batch_size=25, shuffle=False)
    # Sample wise prediction on each set to see performance.

    # ---
    # Load the model.
    device = torch.device("cpu")
    # device = torch.device("cpu")

    ges_mpnn = mpnn.MPNN()
    best_model_path = f"./model_mpnn/ges_mpnn_model.pt"
    ges_mpnn.load_state_dict(torch.load(best_model_path, map_location=device))
 
    with torch.no_grad():
        ges_mpnn.eval()     # Set layers to evaluation mode.

        d1_pred = []

        # Prediction on training.
        for batch in d1_loader:
            batch.to(device)            # Push data to CPU/GPU memory; 
            outputs = ges_mpnn.latent_forward(batch)   # Make prediction for current batch;
            d1_pred.append(outputs)
        
        d1_pred = torch.cat(d1_pred)
        
        d2_pred = []

        for batch in d2_loader:
            batch.to(device)            # Push data to CPU/GPU memory; 
            outputs = ges_mpnn.latent_forward(batch)   # Make prediction for current batch;
            d2_pred.append(outputs)
        
        d2_pred = torch.cat(d2_pred)

    d1_pred = d1_pred.cpu().detach().numpy()
    d2_pred = d2_pred.cpu().detach().numpy()

    print(d1_pred.shape)
    print(d2_pred.shape)
    
    numpy.save("./model_latent/d1_latent.npy", d1_pred)
    numpy.save("./model_latent/d2_latent.npy", d2_pred)
