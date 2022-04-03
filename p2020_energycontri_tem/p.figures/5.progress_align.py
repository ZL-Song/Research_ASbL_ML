# prepare the dat for plotting
# Zilin Song 23NOV2019
#

import numpy as numpy
import subprocess as subp

def load_progress(basis):
    '''load 1d prog data.
    numpy.array of shape (18, 50), reshape to (900,)
    '''
    indir = './aligned_prog_{0}.npy'.format(basis)
    return numpy.load(indir).reshape(900,).tolist()

def load_pert_importance(basis, method, which_feature, ):
    '''load all importance for 900 conformations
    '''
    pert_list = []

    for ds_id in range(18):
        pert_list += [0, ]
        indir = '../../9.fitting-man/2.testing/{0}.ml_test/{1}/ds_{2}.pert.npy'.format(
            basis, method, str(ds_id)
        )
        pert_list += numpy.load(indir).tolist()[which_feature]
        pert_list += [0, ]
    return pert_list

def get_stat(prog_list, pert_list):
    '''slice lists into piece of regions. 
    get stat: average, max, min in region
    return a list of lists
    [x_position, average, max, min, ]
    
    '''
    if len(prog_list) != len(pert_list):
        print('prog and pert list length not equal.\n')
        print(len(prog_list))
        print(len(pert_list))
        exit()

    stat_result = []
    n = 20 # number of slices

    for x in range(n):
        lower = round(0.10 * x, 2)
        upper = round(0.10 * (x+1), 2)
        included_pert_list = []
        path_count_list = []

        for i in range(len(prog_list)):
            
            if prog_list[i] >= lower and prog_list[i] < upper:
                included_pert_list.append(pert_list[i])

                if not (i // 50) in path_count_list:
                    path_count_list.append(i // 50)
                
        stat = None
        if len(included_pert_list) > 0:
            max_pert = max(included_pert_list)
            min_pert = min(included_pert_list)
            average_pert = sum(included_pert_list) / len(included_pert_list)
            
            stat = [
                round(0.10 * x + 0.05, 3),
                round(average_pert, 4), 
                round(max_pert - average_pert, 4), 
                abs(round(min_pert - average_pert, 4)), 
                ]
        if stat != None:
            stat_result.append(stat)
    
    return stat_result

def main(basis, method, ):
    fids = [f for f in range(9)]

    stat_list = []
    for fid in fids:
        prog = load_progress(basis)
        pert = load_pert_importance(basis, method, fid, )
        stat_list.append(get_stat(prog, pert))

    subp.call('mkdir -p perprog_{0}'.format(basis), shell=True)
    numpy.save('perprog_{0}/{1}_stat'.format(basis, method, ), stat_list)

if __name__ == "__main__":

    for basis in ['631++Gdp']: # ['sccdftb', '631G', '631+Gd', '631++Gdp', 'dftd631++Gdp', '6311++Gdp', 'dftd6311++Gdp']: 

        for model in ['svr', 'gpr', 'krr']:
            main(basis, model)
