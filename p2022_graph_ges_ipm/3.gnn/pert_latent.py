# Make predictions with a MPNN model on all dataset with ordered data entries.
# Zilin Song, 21 Mar 2022
# 

import io_gesdata, mpnn
import numpy
import torch
from torch_geometric.data import Data

def get_model():
    ges_mpnn = mpnn.MPNN()
    best_model_path = f"./model_mpnn/ges_mpnn_model.pt"
    ges_mpnn.load_state_dict(torch.load(best_model_path, map_location=torch.device("cuda:0" if torch.cuda.is_available() else "cpu")))
    return ges_mpnn

def predict(model, d):
    x, edge_index, edge_attr = d.x, d.edge_index, d.edge_attr
    batch = torch.zeros(x.shape[0], dtype=int, device=x.device) # d is a single graph
    with torch.no_grad():
        model.eval()
        y_latent = model.pert_forward(batch, x, edge_index, edge_attr)

    return y_latent

def remove_edge(d, rm_indices):
    """Remove edge_index from data.
    Note that rm_indices includes the indices of two edges to be removed.
    """
    x, edge_index, edge_attr, y = d.x, d.edge_index, d.edge_attr, d.y

    # Create new edge connectivities
    mask = torch.ones(edge_index.shape[1], dtype=bool)
    mask[rm_indices] = False

    edge_index = edge_index[:, mask]
    edge_attr  = edge_attr[mask, :]

    return Data(x=x, edge_index=edge_index, edge_attr=edge_attr, y=y)

if __name__ == '__main__':
    d1, d2 = io_gesdata.load_ges_data(split=False)
    d1_edge_count = 54  # number of edges in each set. 
    d2_edge_count = 60
    edge_labels = numpy.load("../2.datasets/rawds/label_edges.npy")

    ges_mpnn = get_model()

    d1_pert_latent = []

    for d in range(len(d1)):
        ref_latent = predict(ges_mpnn, d1[d])
        pert_latent_list = []

        for edge_i in range( int(d1_edge_count/2) ):

            new_d = remove_edge(d1[d], torch.tensor([edge_i*2, edge_i*2+1]))
            pert_latent = predict(ges_mpnn, new_d)
            diff_latent = pert_latent - ref_latent

            pert_latent_list.append(diff_latent.cpu().detach().numpy())
            pert_latent_list.append(diff_latent.cpu().detach().numpy())
            
            print(f"D1 {d}, {edge_labels[edge_i]} ")

        d1_pert_latent.append(pert_latent_list)
    
    d2_pert_latent = []
    
    for d in range(len(d2)):
        ref_latent = predict(ges_mpnn, d2[d])
        pert_latent_list = []

        for edge_i in range( int(d2_edge_count/2) ):

            new_d = remove_edge(d2[d], torch.tensor([edge_i*2, edge_i*2+1]))
            pert_latent = predict(ges_mpnn, new_d)
            diff_latent = pert_latent - ref_latent

            pert_latent_list.append(diff_latent.cpu().detach().numpy())
            pert_latent_list.append(diff_latent.cpu().detach().numpy())
            
            print(f"D2 {d}, {edge_labels[edge_i]} ")

        d2_pert_latent.append(pert_latent_list)

    d1_pert_latent = numpy.squeeze(numpy.asarray(d1_pert_latent), axis=2)
    d2_pert_latent = numpy.squeeze(numpy.asarray(d2_pert_latent), axis=2)
    
    print(d1_pert_latent.shape)
    print(d2_pert_latent.shape)

    numpy.save(f"./model_latent_pert/d1_pert_latent.npy", d1_pert_latent)
    numpy.save(f"./model_latent_pert/d2_pert_latent.npy", d2_pert_latent)
