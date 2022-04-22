# batch plot figues.
# Song.
# 

import numpy, matplotlib, math
import matplotlib.pyplot as plt

import seaborn as sns
sns.set_theme()

def ds_load(sys, path, ):
    '''sys: 'toho_amp', 'toho_cex';
    path: 'r1ae', 'r2ae';
    ds:   'test', 'train', 'total'.
    '''
    ydir     = f'/users/zilins/scratch/2.proj_toho2lig_acy/2.datasets/4.conclude_ds/fin_ds/{sys}.{path}.y.npy'

    tag = 0 if sys == 'toho_amp' and path == 'r1ae' else \
          1 if sys == 'toho_cex' and path == 'r1ae' else \
          2 if sys == 'toho_amp' and path == 'r2ae' else \
          3 if sys == 'toho_cex' and path == 'r2ae' else \
          4 if sys == 'both'     and path == 'r1ae' else \
          5 if sys == 'both'     and path == 'r2ae' else \
          None

    ypreddir = f'/users/zilins/scratch/2.proj_toho2lig_acy/3.dwnn/cpu_mod{tag}/y_pred.npy'

    return numpy.load(ydir).flatten(), numpy.load(ypreddir).flatten()

fo_log = open('dwnn_performance_stat.log', 'w')

for path in ['r1ae', 'r2ae', ]:
    for sys in ['toho_amp', 'toho_cex', 'both']:
        fo_log.write('\n{0}.{1}\n\n'.format(sys, path, ))
                
        # init figure ==================================================================
        sns.set_style(style='white')
        sns.set_style("ticks")
        fig, ax,  = plt.subplots(figsize=(6, 6), dpi=900, )
        plt.subplots_adjust(left=1.5/6, right=5.5/6, bottom=1/6, top=5/6, )

        ax.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(base=20.0))
        ax.yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(base=20.0))
        ax.tick_params(which='major', direction='in', length=6, width=1, labelsize='x-large', )

        ax.set_xlabel(r'$E_{ML}$'+r' $(kcal$ $mol^{-1})$', fontsize='xx-large', )
        ax.set_ylabel(r'$E_{QM/MM}$'+r' $(kcal$ $mol^{-1})$', fontsize='xx-large', )
        # legend labels:

        # load pathway data ================================================================
        calc, pred = ds_load(sys, path)
                
        # red line
        mx =  80. # math.ceil( max(numpy.max(calc), numpy.max(pred), ) / 20.) * 20.
        mn = -40. # math.floor(min(numpy.min(calc), numpy.min(pred), ) / 20.) * 20.
        ax.plot(numpy.linspace( mx, mn, 2, ), numpy.linspace( mx, mn, 2, ), 
                c=sns.color_palette('colorblind')[3],  label='Fitting target', lw=1, zorder=2)

        # scatters
        ax.scatter(pred, calc, s=1, color='k', zorder=1)

        # raw string of metrics
        rstr_r2 = r'$R^2$'
        rstr_mae = r'$MAE$'
        rstr_rmse = r'$RMSE$'
        rstr_nsamp = r'$n_{samples}$'
        # metrics
        r2   = numpy.corrcoef(calc, pred)[0, 1]**2
        mae  = numpy.abs(calc - pred).mean() 
        rmse = numpy.square(calc - pred).mean() ** 0.5 
        n    = calc.shape[0]

        # display metrics on figure
        ax.text(0.96, 0.04, 
                f'{rstr_r2: >10} = {r2: <8.4f}\n{rstr_mae: >10} = {mae: <8.4f}\n{rstr_rmse: >10} = {rmse: <8.4f}\n{rstr_nsamp: >10} = {n: <8}', 
                ha='right', va='bottom', transform=ax.transAxes, fontsize=18)

        # label of system
        syslbl = sys[0].upper() + sys[1:4].lower() + sys[4:].replace('_', '/').upper() + ': ' + path[:2].upper() + '-' + path[2:].upper() if sys != 'both' else \
                 'Toho/AMP&CEX: '+path[:2].upper() + '-' + path[2:].upper()
        ax.text(0.04, 0.96, syslbl, ha='left', va='top', transform=ax.transAxes, fontsize=18)

        # log
        fo_log.write(f'{rstr_r2: >10} = {r2: <8.4f}\n{rstr_mae: >10} = {mae: <8.4f}\n{rstr_rmse: >10} = {rmse: <8.4f}\n{rstr_nsamp: >10} = {n: <8}')
                    
        ax.set_aspect(1.)   
        fig.savefig(f'{sys}.{path}.png')
        
        print(f'Done: {sys}.{path}.png')
        fo_log.write('\n')
fo_log.write('\n')
