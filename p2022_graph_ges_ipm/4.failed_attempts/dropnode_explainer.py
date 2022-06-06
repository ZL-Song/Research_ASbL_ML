# Implements the DropNodeExplainer
# Zilin Song, 1 Feb 2022
# 

import math, sys
import mpnn, io_gesdata
import torch, numpy

from torch_geometric.nn import MessagePassing

class SuspendNodeExplainer(torch.nn.Module):

    def __init__(self, model, epochs:int=2000, lr:float=0.01):
        super().__init__()
        self.model = model
        self.epochs = epochs
        self.lr = lr

    def __repr__(self):
        return f'{self.__class__.__name__}()'
        
    def __set_masks__(self, x, edge_index, susp_node_index):
        """Here sets several node masks for modifying input representation."""
        # The mask to be trained for adjusting the node representations
        self.node_mask = torch.nn.Parameter(torch.ones(x.size()[0], 1), requires_grad=True)

        # The mask that acts as the selector for which node to exclude from the above mask.
        self.node_susp_mask = torch.ones(x.size()[0], 1)
        self.node_susp_mask[susp_node_index] = 0
        
        # The mask that I don't know what they really do in the PyG.MessagePassing() base class, 
        # Do they scale the edge attributes without removing the linkage as what GNNExplainer() expects? 
        # Or do they block the linkage in adj_mat as what I expect? 
        # I am graduating in May so no time to dig around... Will look into in the future. edit: will **NOT** lol.
        # To be safe, I rather instead removed the edges by creating new graph than setting the edge_masks.
        self.edge_mask = torch.ones(edge_index.size(1))
        self.loop_mask = edge_index[0] != edge_index[1]

        for module in self.model.modules():
            if isinstance(module, MessagePassing):
                module.__explain__   = True
                module.__edge_mask__ = self.edge_mask
                module.__loop_mask__ = self.loop_mask

    def __clear_masks__(self):
        for module in self.model.modules():
            if isinstance(module, MessagePassing):
                module.__explain__   = False
                module.__edge_mask__ = None
                module.__loop_mask__ = None

        self.node_mask = None
        self.node_susp_mask = None
        self.edge_mask      = None
        self.loop_mask      = None

    def __loss__(self, out, pred):
        return torch.cdist(out, pred)

    def __remove_edge__(self, dropnode_idx, edge_index, edge_attr):
        """Create a graph that removes all linkages around a node."""
        # Find the edge indices that contains the susp_node_index, return a 1D tensor of shape (num_of_all_edges).
        # 0 means the edge does not link the selected node; 
        # 1 ..... ... .... does     link the selected node.
        drop_edge_mask  = torch.sum(torch.where(edge_index==dropnode_idx, 1, 0), dim=0)
        # Drop the edges with the linkage.
        drop_edge_index = edge_index[:, drop_edge_mask==0]
        drop_edge_attr  = edge_attr[drop_edge_mask==0, :]

        return drop_edge_index, drop_edge_attr
        
    def explain_graph(self, graph_data, susp_node_index):
        """Explain a single graph."""
        # Unpack the complete graph_data
        full_x, full_edge_index, full_edge_attr = graph_data.x, graph_data.edge_index, graph_data.edge_attr
        # Should contain only 1 graph.
        batch = torch.zeros(full_x.shape[0], dtype=int, device=full_x.device)
        
        # Get the initial prediction.
        self.model.eval()
        self.__clear_masks__()

        with torch.no_grad():
            prediction        = self.model.explain_forward(x=full_x, edge_index=full_edge_index, edge_attr=full_edge_attr, batch=batch)

        # Get the edge representations that droped all linkages around the specified node.
        # drop_edge_index, drop_edge_attr = self.__remove_edge__(susp_node_index, full_edge_index, full_edge_attr)
        drop_edge_index, drop_edge_attr = self.__remove_edge__(susp_node_index, full_edge_index, full_edge_attr)

        # Set the node masks for learning.
        self.__set_masks__(full_x, drop_edge_index, susp_node_index)

        self.to(full_x.device)

        optimizer = torch.optim.Adam([self.node_mask], lr=self.lr)

        for epochs in range(1, self.epochs + 1):
            optimizer.zero_grad()
            h = full_x * self.node_mask * self.node_susp_mask

            out = self.model.explain_forward(x=h, edge_index=drop_edge_index, edge_attr=drop_edge_attr, batch=batch)

            loss = self.__loss__(out, prediction)
            loss.backward()

            optimizer.step()

        node_mask = self.node_mask.detach().squeeze()
        edge_mask = self.edge_mask.detach()

        self.__clear_masks__()
        return node_mask, edge_mask, loss[0].item()


def map_explain(datalist):
        # Load the model to be explianed.
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    # device = torch.device("cpu")
    
    ges_mpnn = mpnn.MPNN()
    best_model_path = f"./model_mpnn/ges_mpnn_model.pt"
    ges_mpnn.load_state_dict(torch.load(best_model_path, map_location=torch.device("cuda:0" if torch.cuda.is_available() else "cpu")))

    # make explainer
    explainer = SuspendNodeExplainer(ges_mpnn)
    
    ges_mpnn.to(device)
    explainer.to(device)

    node_explained = []
    edge_explained = []


    for i in range(1, 2):
        data = datalist[i]
        node_fmask, edge_fmask, importance = explainer.explain_graph(data, 19)

        node_explained.append(node_fmask.numpy())
        edge_explained.append(edge_fmask.numpy())
        # print(node_fmask, loss, importance, flush=True)
        
        print(f"Explaining {i:5}  {node_fmask} {importance:20}...", flush=True)
        # print(edge_fmask)

    return node_explained, edge_explained

    

if __name__ == '__main__':
    
    # ---
    # Load data list.
    d1, d2= io_gesdata.load_ges_data(split=False)

    # repeat for 10 times for each instance
    i = sys.argv[1]

    # n_d1, e_d1 = map_explain(d1)
    n_d2, e_d2 = map_explain(d2)

    # numpy.savez(f"./explained_mpnn/explained_d1_round{i}.npz", n_d1=n_d1, e_d1=e_d1)
    # numpy.savez(f"./explained_mpnn/explained_d2_round{i}.npz", n_d2=n_d2, e_d2=e_d2) 
