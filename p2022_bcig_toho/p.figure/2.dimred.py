# Dimensionality reduction.
# Zilin Song. 1 SEPT 2021
# 

import numpy
from sklearn.decomposition import PCA


def load_fpw():
    '''Load and concat the all pairwise ds
    '''
    pw_all = numpy.load('../../2.datasets/1.merge_ds/hvypw_rel/hvypw_rel_ds.npy')
    return pw_all

def dr(ds, ):
    '''Do PCA.
    '''
    pca = PCA(n_components=2)

    ds_pca = pca.fit_transform(ds)
    return ds_pca[:, 0], ds_pca[:, 1]

def process():
    '''fall'''
    fpw = load_fpw()
    print(fpw.shape)
    fpw_pc1, fpw_pc2 = dr(fpw)
    numpy.save(f'./pw_pc1.npy', fpw_pc1)
    numpy.save(f'./pw_pc2.npy', fpw_pc2)
    
if __name__ == '__main__':
    process()