# Some not-so-succesful attempts. 

Zilin Song, 2022 Mar 14

**NOTE: I do not aim to criticize GNNExplainer or related methods in this document,  
nor should this document be used for supporting/against any of the related methods noted below.  
This doc was provided only in the hope that it could help with other researches on related topics.**

Far as what I know, GNNExplainer is the pioneering "first-in-class" explanation methods for GNN models,  
no method can be perfect but all these attemps and efforts will pave the foundation to perfection (hopefully).   

--- 

I coded a few GNNExplainer-alike approaches for explain the GNN I made for GES/IPM deacylation.  

An intuitive explanation to the GNNExplainer method would be...  

Briefly, GNNExplainer attempts to learn a mask that "mask out" trivial features to the model output.  
This is done by frozen the model weights and learn a weight tensor (the feature mask) which is multiplied directly to the input node features.  
Training such model is to learn a mask that "mask out" as much feature dimensions as possible (nodes or node-features, as in the original paper), as long as the model produces the ~same output.  

This mask will tell us what node or node-features are trivial to the model output. 

---

- This approach will very likely **NOT** work on Regression tasks (as in my case).

  Explanations of regression models from this approach is heavily biased by "introduced evidence" (or something called similar, I read it somewhere).  
  That is, for regression models one could easily find two feature input (x1 and x2=w*x1) that produces the same output, (consider the case of higher-order polynomial).  
  We can easily break GNNExplaner on a 3rd-order polynomial fit with appropriate numerical setups (i.e. initialize the mask at appropriate coordinates).  

- This approach **WILL** very likely work on Classification tasks, this has been demonstrated by the authors in their GNNExplainer paper.   
  
  Classification task can be viewed as the attempt to draw boundaries in a model-learned latent space.  
  Explanation from GNNExplainer can be viewed as the likeliness of crossing classification boundaries by change a feature input to a certain extent (the weight).  
  Such application will also be biased by "introduced evidence" but it will work b/c classification output is not as sensitive to the displacement of the latent.  
  I think it will work with certain datasets and models that does not produce a very dense and complicated latent representation.  

---

What I did in the python scripts under this dir ("- failed" in bulletins below means no reasonable explanation is found):
Note that mine was a regression task.  

1. After finding that the GNNExplainer in pytorch_geometric does not give reasonable explaination on the NODEs (node mask only - failed);  
2. I coded some thing (not shown in here) to mask the edges (edge mask only - failed);  
3. I thought it was b/c the edge and nodes has to be somewhat correlated, thus I then did: remove an edge from the graph then optimize for the edge mask to compensate the loss of a edge (drop-one-edge then edge mask - failed);  
4. I then drop all edge around one node (block the linkage of a node), then optimize for edge mask (block-node then edge mask - failed), this is the code in the dropnode_explainer.py file.  
 
None of these attempts made reasonable explanations for my model.  

---

Relatedly, the results of GNNExplainer or any model I coded above depends on how/where the weight mask was initialized.  
The original authors initialized weights from a normal distribution centered at 0.5. This will leads to unstable results (sometimes controdicted results). 

There has been a "issue post" in the pytorch_geometric repo: https://github.com/pyg-team/pytorch_geometric/issues/1985.
demonstrating the unstability of the GNNExplainer approach... (But I think it is really just b/c the weight masks are initialized randomly)  

I tried to initialize all masks with all zeros/0.5/ones, or from a normal distribution around zeros/0.5/ones, but non of them provided reasonable explanations.  

---
References. 
1. Pytorch geomtric doc and implementation of GNNExplainer: https://pytorch-geometric.readthedocs.io/en/latest/_modules/torch_geometric/nn/models/gnn_explainer.html#GNNExplainer ;
2. Paper GNNExplainer:	arXiv:1903.03894