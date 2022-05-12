# Training a MPNN model
# Zilin Song, 19 Jan 2022
# 
import io_gesdata, mpnn

import random

import torch
import torch.nn.functional as F

from torch.utils.data import random_split
from torch_geometric.loader import DataLoader

if __name__ == '__main__':
    # ---
    # Load data list.
    train_set, valid_set = io_gesdata.load_ges_data()

    # ---
    # Make data loaders
    training_loader = DataLoader(train_set, batch_size=25, shuffle=True)
    validate_loader = DataLoader(valid_set, batch_size=25, shuffle=True)

    # ---
    # Net, device, optimizer.
    ges_mpnn = mpnn.MPNN()

    device    = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    optimizer = torch.optim.Adam(ges_mpnn.parameters(), lr=0.001)

    ges_mpnn.to(device) # Push mpnn to CPU/GPU memory.

    # ---
    # Training.
    epochs = 750
    best_model_path = f"./model_mpnn/ges_mpnn_model.pt"
    validation_best_loss = 9999.

    for epoch in range(epochs):
        # Training.
        train_loss  = 0.
        batch_count = 0
        ges_mpnn.train()                # Set mpnn to training mode.

        for batch in training_loader:
            # Training.
            batch.to(device)            # Push data to CPU/GPU memory; 
            optimizer.zero_grad()       # Zero gradients for every batch; 
            outputs = ges_mpnn(batch)   # Make prediction for current batch;
            loss = F.mse_loss(outputs, batch.y.unsqueeze(1))    # Compute the loss; 
            loss.backward()             # Compute gradients along the nn graph; 
            optimizer.step()            # Adjust learning weights.

            # Stats.
            train_loss  += loss.item()
            batch_count += 1

        training_avg_loss = train_loss / batch_count

        # Validation.
        valid_loss  = 0.
        batch_count = 0
        ges_mpnn.eval()                 # Set mpnn to evaluation mode.
            
        for batch in validate_loader:
            batch.to(device)            # Push data to CPU/GPU memory; 
            outputs = ges_mpnn(batch)   # Make prediction for current batch;
            loss = F.mse_loss(outputs, batch.y.unsqueeze(1))    # Compute the loss; 

            # Stats.
            valid_loss += loss.item()
            batch_count += 1

        validation_avg_loss = valid_loss / batch_count
        
        # Save model with best performance.
        if validation_avg_loss <= validation_best_loss and epoch >= 200:
            validation_best_loss = validation_avg_loss
            torch.save(ges_mpnn.state_dict(), best_model_path)

        print(f"Epochs: {epoch} |", 
              f"Training avg. loss: {training_avg_loss:.4f} |", 
              f"Validation avg. loss: {validation_avg_loss:.4f} |",
              f"Best Validation loss: {validation_best_loss:.4f} |", 
            )
