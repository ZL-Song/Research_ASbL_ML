# MPNN for learning Ges graph_data.
# Zilin Song, 19 Jan 2022
# 

import torch
import torch.nn as nn
import torch.nn.functional as F

from torch_geometric.nn import NNConv, global_add_pool

class MPNN(torch.nn.Module):
    r"""A message passing network."""

    def __init__(self, num_node_features=4, num_edge_features=1):
        r"""A message passing network.
        num_node_features: number of node features on the nodes. 
        num_edge_features: number of edge features on the edges.

        NNConv is alias to ECConv - Edge-conditioned graph convolution.
	"""
        super().__init__()
        # convn_net variables: a nn that maps edge features [-1, num_edge_features] 
        #                      to shape [-1, in_channels * out_channels]
        conv1_net = nn.Sequential(nn.Linear(num_edge_features, 64                  ), nn.PReLU(),
                                  nn.Linear(64,                num_node_features*64))
        conv2_net = nn.Sequential(nn.Linear(num_edge_features, 64                  ), nn.PReLU(),
                                  nn.Linear(64,                64*64               ))
        conv3_net = nn.Sequential(nn.Linear(num_edge_features, 64                  ), nn.PReLU(),
                                  nn.Linear(64,                64*64               ))


        self.conv1 = NNConv(num_node_features, 64, conv1_net)
        self.conv2 = NNConv(64,                64, conv2_net)
        self.conv3 = NNConv(64,                64, conv3_net)
        self.out   = nn.Linear(64,  1, bias=False)
        self.prelu = nn.PReLU()

    def forward(self, graph_data):
        """Forward pass for training."""
        batch, x, edge_index, edge_attr = graph_data.batch, graph_data.x, graph_data.edge_index, graph_data.edge_attr
        x = self.prelu(self.conv1(x, edge_index, edge_attr))
        x = self.prelu(self.conv2(x, edge_index, edge_attr))
        x = self.prelu(self.conv3(x, edge_index, edge_attr))
        x = global_add_pool(x, batch)
        # x = F.relu(self.fc_1(x))
        output = self.out(x)
        return output
    
    # def explain_forward(self, x, edge_index, edge_attr, batch):
    #     """Modified for explainer-compatible forward pass."""
    #     x = self.prelu(self.conv1(x, edge_index, edge_attr))
    #     x = self.prelu(self.conv2(x, edge_index, edge_attr))
    #     x = self.prelu(self.conv3(x, edge_index, edge_attr))
    #     x = global_add_pool(x, batch)
    #     # x = F.relu(self.fc_1(x))
    #     output = self.out(x)
    #     return output

    def latent_forward(self, graph_data):
        """Modified for latent-outputing forward pass."""
        batch, x, edge_index, edge_attr = graph_data.batch, graph_data.x, graph_data.edge_index, graph_data.edge_attr
        x = F.relu(self.conv1(x, edge_index, edge_attr))
        x = F.relu(self.conv2(x, edge_index, edge_attr))
        x = F.relu(self.conv3(x, edge_index, edge_attr))
        x = global_add_pool(x, batch)
        return x * self.out.weight

    def pert_forward(self, batch, x, edge_index, edge_attr):
        """Modified for latent-outputing forward pass."""
        x = F.relu(self.conv1(x, edge_index, edge_attr))
        x = F.relu(self.conv2(x, edge_index, edge_attr))
        x = F.relu(self.conv3(x, edge_index, edge_attr))
        x = global_add_pool(x, batch)
        return x * self.out.weight

if __name__ == '__main__':
    
    import io_gesdata, numpy
    from torch_geometric.loader import DataLoader
    # ---
    # Load graph_data list.
    d1, d2 = io_gesdata.load_ges_data(split=False)

    # ---
    # Make graph_data loaders
    d1_loader = DataLoader(d1, batch_size=25, shuffle=False)
    d2_loader = DataLoader(d2, batch_size=25, shuffle=False)
    # Sample wise prediction on each set to see performance.

    # ---
    # Load the model.
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    # device = torch.device("cpu")

    ges_mpnn = MPNN()
    best_model_path = f"./model_mpnn/ges_mpnn_model.pt"
    ges_mpnn.load_state_dict(torch.load(best_model_path, map_location=torch.device("cuda:0" if torch.cuda.is_available() else "cpu")))
 
    with torch.no_grad():
        ges_mpnn.eval()     # Set layers to evaluation mode.

        d1_pred = []

        # Prediction on training.
        for batch in d1_loader:
            batch.to(device)            # Push graph_data to CPU/GPU memory; 
            outputs, w  = ges_mpnn.latent_forward(batch.x, batch.edge_index, batch.batch, batch.edge_attr)   # Make prediction for current batch;
            outputs2    = ges_mpnn.forward(batch.x, batch.edge_index, batch.batch, batch.edge_attr)   # Make prediction for current batch;
            
        print(outputs.cpu().detach().numpy()[0])
        print(outputs.cpu().detach().numpy()[1])
        print(outputs.cpu().detach().numpy()[2])

        a = numpy.sum(outputs.cpu().detach().numpy()[:3], axis=1)
        b = outputs2.cpu().detach().squeeze().numpy()[:3]

        a = outputs.cpu().detach()[:3]
        b = outputs2.cpu().detach().squeeze()[:3]
        q = a * w
        print(numpy.sum(q.cpu().detach().numpy(), axis=1))
        print(w.shape)
        print(a.shape)
        print(b)
