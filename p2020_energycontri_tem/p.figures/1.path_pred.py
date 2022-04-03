# plot calculated path with corresponding predicted path.
# Zilin Song, 11NOV2019
# 
import matplotlib.pyplot as plt
import subprocess as subp
import numpy as numpy
from pylab import figure, text, scatter, show

def get_pred_path(basis, ds_id, model_name):
    '''load predicted pathway and return as a list.
    a list of 50 floats.
    '''
    indir = '../../8.0.prediction-man/2.testing/{0}.ml_test/ds_{1}/{2}/y_pred.npy'.format(
        basis, ds_id, model_name, 
    )
    return numpy.load(indir).tolist()
    
def get_calc_path(basis, ds_id, ):
    '''load calculated pathway and return as a list.
    a list of 50 floats.
    '''
    indir = '../../6.data.prepare/3.dataset.conclude/{0}.path_dat/ds_{1}.y_test.npy'.format(
        basis, ds_id, 
    )
    return numpy.load(indir).tolist()

def build_out_filename(basis, ds_id, ):
    '''establish the directory for storing the plotted data.
    also builds the output dir by 'mkdir'
    '''
    outdir = '{0}.path'.format(basis, )
    subp.call('mkdir -p {0}'.format(outdir, ), shell=True)
    return '{0}/{1}_ds_{2}.png'.format(outdir, basis, ds_id, )

def plot_fig(basis, ds_id, ):
    '''plot the figure and save.
    '''
    # load data
    svr_pred_path = get_pred_path(basis, ds_id, 'svr', )
    gpr_pred_path = get_pred_path(basis, ds_id, 'gpr', )
    krr_pred_path = get_pred_path(basis, ds_id, 'krr', )
    calc_path = get_calc_path(basis, ds_id, )

    # state char
    ds_ids = [i for i in range(18)]
    stt_char = 'r' if (ds_id in ds_ids[0:5]) else 't' if (ds_id in ds_ids[6:11]) else 'p'

    # color & linestyles
    colors = [(230,  25,  75, ),
              ( 60, 180,  75, ),
              (  0, 130, 200, ),
              (170, 110,  40, ),
             ]
    colors = [(float(r/255), float(g/255), float(b/255),) for r,g,b in colors]
    
    fig, ax = plt.subplots(figsize=(7, 3), dpi=300)

    # spine
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_linewidth(1)
    ax.spines['left'].set_linewidth(1)

    # x axis
    ax.set_xlim(0, 51)
    ax.xaxis.set_major_locator(plt.MultipleLocator(25))
    ax.xaxis.set_minor_locator(plt.MultipleLocator(5))

    # y axis
    ax.set_ylim(-40, 23)
    ax.yaxis.set_major_locator(plt.MultipleLocator(20))
    ax.yaxis.set_minor_locator(plt.MultipleLocator(10))

    # tick & labels on x and y
    ax.tick_params(which='major', direction='out', length=5, width=1)
    ax.tick_params(which='minor', direction='out', length=3, width=1)
    #ax.tick_params(which='both', labelleft=False, labelbottom=False, )

    # # x label and y label
    ax.set_xlabel('Replica Number', ) 
    ax.set_ylabel('Energy (kcal $\mathregular{mol^{-1}}$)', )

    lw = 1.5
    ms = 5
    # y = 0 line
    ax.plot([0.0, 51], [0.0, 0.0], c = 'grey', linewidth=lw)
    ax.plot([repno for repno in range(1, 51)],
            calc_path, '.-',
            c='k',
            markersize=ms, 
            linewidth=lw, 
            label='Calculated'.format(
                ds_id, stt_char,
                )
    )
    ax.plot([repno for repno in range(1, 51)],
            svr_pred_path, '.-',
            c=colors[0], 
            markersize=ms, 
            linewidth=lw, 
            label='SVR predicted'
    )
    ax.plot([repno for repno in range(1, 51)],
            gpr_pred_path, '.-', 
            c=colors[2], 
            markersize=ms,
            linewidth=lw, 
            label='GPR predicted'
    )
    ax.plot([repno for repno in range(1, 51)],
            krr_pred_path, '.-', 
	    c=colors[3], 
            markersize=ms, 
            linewidth=lw, 
            label='KRR predicted'
    )
    basis_name = 'what the fuck ?'
    if basis == 'sccdftb':
        basis_name = 'DFTB3/mio:CHARMM'
    elif basis == '631G':
        basis_name = 'B3LYP/6-31G:CHARMM'
    elif basis == '631+Gd':
        basis_name = 'B3LYP/6-31+G*:CHARMM'
    elif basis == '631++Gdp':
        basis_name = 'B3LYP/6-31++G**:CHARMM'
    elif basis == 'dftd631++Gdp':
        basis_name = 'B3LYP-D3/6-31++G**:CHARMM'
    elif basis == '6311++Gdp':
        basis_name = 'B3LYP/6-311++G**:CHARMM'
    elif basis == 'dftd6311++Gdp':
        basis_name = 'B3LYP-D3/6-311++G**:CHARMM'

    #fig.savefig('dftb3_16.png')
    
    text(0.98, 0.95,
        '{0}: {1}/{2}'.format(basis_name, ds_id, stt_char, ),
        transform=ax.transAxes, 
        verticalalignment='top', 
        horizontalalignment='right', )

    leg = ax.legend(loc="lower left", bbox_to_anchor=(0.04, 0.04), ncol=1)
    leg.get_frame().set_linewidth(0.0)
    
    plt.tight_layout()
    fig.savefig(build_out_filename(basis, ds_id, ))


def main():
    basis_list =  ['sccdftb', '631G', '631++Gdp', '631+Gd', 'dftd631++Gdp', '6311++Gdp', 'dftd6311++Gdp'] 
    ds_ids = [i for i in range(18)]
    
    # plot_fig('sccdftb', 16)
    
    for b in basis_list:
        for i in ds_ids:
            print('Processing... {0:10}{1:<5}'.format(b, i, ))
            plot_fig(b, i, )

if __name__ == "__main__":
    main()
