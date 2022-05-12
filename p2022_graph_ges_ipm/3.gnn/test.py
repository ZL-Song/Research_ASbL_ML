# Make predictions with a MPNN model on training/validation set.
# Zilin Song, 19 Jan 2022
# 
from scipy.stats import linregress
import io_gesdata, mpnn
import numpy

import torch
import torch.nn.functional as F

from torch_geometric.loader import DataLoader

if __name__ == '__main__':
    # ---
    # Load data list.
    train_set, valid_set = io_gesdata.load_ges_data()

    # ---
    # Make data loaders
    training_loader = DataLoader(train_set, batch_size=25, shuffle=False)
    validate_loader = DataLoader(valid_set, batch_size=25, shuffle=False)
    # Sample wise prediction on each set to see performance.

    # ---
    # Load the model.
    ges_mpnn = mpnn.MPNN()
    best_model_path = f"./model_mpnn/ges_mpnn_model.pt"
    ges_mpnn.load_state_dict(torch.load(best_model_path))

    device    = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    ges_mpnn.to(device)
    
    with torch.no_grad():
        ges_mpnn.eval()     # Set layers to evaluation mode.

        ytrain_pred = []
        ytrain      = []

        # Prediction on training.
        for batch in training_loader:
            batch.to(device)            # Push data to CPU/GPU memory; 
            outputs = ges_mpnn(batch)   # Make prediction for current batch;
            ytrain_pred.append(outputs)
            ytrain.append(batch.y.unsqueeze(1))
        
        ytrain_pred = torch.cat(ytrain_pred)
        ytrain      = torch.cat(ytrain)
        
        yvalid_pred = []
        yvalid      = []

        for batch in validate_loader:
            batch.to(device)            # Push data to CPU/GPU memory; 
            outputs = ges_mpnn(batch)   # Make prediction for current batch;
            yvalid_pred.append(outputs)
            yvalid.append(batch.y.unsqueeze(1))
        
        yvalid_pred = torch.cat(yvalid_pred)
        yvalid      = torch.cat(yvalid)

        print(F.mse_loss(ytrain_pred, ytrain).item()**0.5)
        print(F.mse_loss(yvalid_pred, yvalid).item()**0.5)

    d1_train = numpy.squeeze(ytrain[:425].cpu().detach().numpy(), axis=1)
    d2_train = numpy.squeeze(ytrain[425:].cpu().detach().numpy(), axis=1)
    d1_valid = numpy.squeeze(yvalid[:75].cpu().detach().numpy(),  axis=1)
    d2_valid = numpy.squeeze(yvalid[75:].cpu().detach().numpy(),  axis=1)

    d1_train_pred = numpy.squeeze(ytrain_pred[:425].cpu().detach().numpy(), axis=1)
    d2_train_pred = numpy.squeeze(ytrain_pred[425:].cpu().detach().numpy(), axis=1)
    d1_valid_pred = numpy.squeeze(yvalid_pred[:75].cpu().detach().numpy(),  axis=1)
    d2_valid_pred = numpy.squeeze(yvalid_pred[75:].cpu().detach().numpy(),  axis=1)

    numpy.save("./model_pred/d1_train.npy", d1_train)
    numpy.save("./model_pred/d2_train.npy", d2_train)
    numpy.save("./model_pred/d1_valid.npy", d1_valid)
    numpy.save("./model_pred/d2_valid.npy", d2_valid)

    numpy.save("./model_pred/d1_train_pred.npy", d1_train_pred)
    numpy.save("./model_pred/d2_train_pred.npy", d2_train_pred)
    numpy.save("./model_pred/d1_valid_pred.npy", d1_valid_pred)
    numpy.save("./model_pred/d2_valid_pred.npy", d2_valid_pred)

    print()
    slope, intercept, r, p, stderr = linregress(d1_train, d1_train_pred)
    print(f"d1 training slope: {slope}, intercept: {intercept}, r^2: {r**2}")

    slope, intercept, r, p, stderr = linregress(d1_valid, d1_valid_pred)
    print(f"d1 validate slope: {slope}, intercept: {intercept}, r^2: {r**2}")

    print("d1 training max:", numpy.max(d1_train-d1_train_pred), "min:", numpy.min(d1_train-d1_train_pred), "avg:", numpy.average(numpy.abs(d1_train-d1_train_pred)))
    print("d1 validate max:", numpy.max(d1_valid-d1_valid_pred), "min:", numpy.min(d1_valid-d1_valid_pred), "avg:", numpy.average(numpy.abs(d1_valid-d1_valid_pred)))
    print()
    slope, intercept, r, p, stderr = linregress(d2_train, d2_train_pred)
    print(f"d2 training slope: {slope}, intercept: {intercept}, r^2: {r**2}")

    slope, intercept, r, p, stderr = linregress(d2_valid, d2_valid_pred)
    print(f"d2 validate slope: {slope}, intercept: {intercept}, r^2: {r**2}")

    print("d2 training max:", numpy.max(d2_train-d2_train_pred), "min:", numpy.min(d2_train-d2_train_pred), "avg:", numpy.average(numpy.abs(d2_train-d2_train_pred)))
    print("d2 validate max:", numpy.max(d2_valid-d2_valid_pred), "min:", numpy.min(d2_valid-d2_valid_pred), "avg:", numpy.average(numpy.abs(d2_valid-d2_valid_pred)))