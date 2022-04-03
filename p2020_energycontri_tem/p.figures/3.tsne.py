# This script does tSNE analysis on conformations
# Zilin Song, 4NOV2019
#

import subprocess as subp
import numpy as numpy
from sklearn.manifold import TSNE

def main():
    basis_list = ['sccdftb', '631G', '631++Gdp']
        
    for basis in basis_list:

        indir = '../../7.feat.sele/2.full.ds.build'.format(basis)

        X = numpy.load('{0}/{1}.X_all.npy'.format(indir, basis))

        tsne = TSNE(n_components=1, 
                    init='pca',
                    method='exact',
                    random_state=0,)
        y = tsne.fit_transform(X)

        print(y)

        numpy.save('{0}.tsne_1d.npy'.format(basis), y)
        
    for basis in basis_list:

        indir = '../../7.feat.sele/2.full.ds.build'.format(basis)

        X = numpy.load('{0}/{1}.X_all.npy'.format(indir, basis))

        tsne = TSNE(n_components=2, 
                    init='pca',
                    method='exact',
                    random_state=0,)
        y = tsne.fit_transform(X)

        print(y)

        numpy.save('{0}.tsne_2d.npy'.format(basis), y)


if __name__ == "__main__":
    main()
